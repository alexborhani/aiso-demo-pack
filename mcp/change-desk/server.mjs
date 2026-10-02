#!/usr/bin/env node
// Meridian's change desk: a small MCP server over stdio for scenario 43 of the demo pack. No dependencies,
// nothing on the network, nothing written to disk. Two tools:
//   request_change        asks the person to confirm before it files anything (MCP elicitation)
//   summarise_change_log  asks the host's model to summarise an asset's change log (MCP sampling); when the
//                         host refuses, it says so and returns the log as it is
// Every change, asset and ticket below is invented.

import { createInterface } from 'node:readline';

const LOG = {
  'MW-300 Halden line 2': [
    '2026-08-04  CHG-2026-0412  Firmware 4.2.1 on the line 2 controller; interlock timer from 400 ms to 250 ms. Reverted 2026-08-06 after three nuisance trips.',
    '2026-08-19  CHG-2026-0447  Bracket for guard sensor GS-2 replaced (cracked). Torque checked to 9 Nm.',
    '2026-09-02  CHG-2026-0471  Coded safety sensor fitted in place of GS-2. Trip count down from 29 to 2 in the following four weeks.',
    '2026-09-23  CHG-2026-0503  Floor cabinet UPS replaced; the old unit reached end of life.',
  ],
  'Riverside test rig': [
    '2026-07-14  CHG-2026-0388  Pressure transducer recalibrated after a 3% drift.',
    '2026-09-11  CHG-2026-0489  Rig PLC clock moved to the plant NTP server.',
  ],
};
const assets = Object.keys(LOG);
const WINDOWS = ['Tonight 22:00', 'Saturday 06:00', 'Next maintenance day'];

const TOOLS = [
  {
    name: 'request_change',
    description: 'File a change request on the Meridian change desk for a plant asset. The desk asks the person to confirm and to pick a change window before anything is filed.',
    inputSchema: {
      type: 'object',
      properties: {
        asset: { type: 'string', enum: assets, description: 'The asset to change' },
        change: { type: 'string', description: 'What will be changed, in one sentence' },
        reason: { type: 'string', description: 'Why, in one sentence' },
      },
      required: ['asset', 'change', 'reason'],
    },
    annotations: { readOnlyHint: false, destructiveHint: false },
  },
  {
    name: 'summarise_change_log',
    description: "Summarise the change log of a plant asset in three sentences. The desk asks the host's model for the summary; when the host does not allow that, the log comes back as it is.",
    inputSchema: {
      type: 'object',
      properties: { asset: { type: 'string', enum: assets, description: 'The asset' } },
      required: ['asset'],
    },
    annotations: { readOnlyHint: true },
  },
];

let nextId = 1;
let ticket = 520;
const waiting = new Map();
const send = (msg) => process.stdout.write(JSON.stringify({ jsonrpc: '2.0', ...msg }) + '\n');
const text = (t, isError = false) => ({ content: [{ type: 'text', text: t }], ...(isError ? { isError: true } : {}) });

/** A request to the client (elicitation or sampling); resolves with its result, rejects with its error. */
function ask(method, params) {
  const id = `desk-${nextId++}`;
  send({ id, method, params });
  return new Promise((resolve, reject) => waiting.set(id, { resolve, reject }));
}

async function requestChange(args) {
  const { asset, change, reason } = args ?? {};
  if (!LOG[asset]) return text(`Unknown asset "${asset}". The desk knows: ${assets.join(', ')}.`, true);
  let answer;
  try {
    answer = await ask('elicitation/create', {
      mode: 'form',
      message: `File a change request on ${asset}: ${change} (${reason}). Confirm, and pick a change window.`,
      requestedSchema: {
        type: 'object',
        properties: {
          confirm: { type: 'boolean', title: 'File this change request', description: 'Nothing is filed unless this is ticked.' },
          window: { type: 'string', title: 'Change window', enum: WINDOWS },
        },
        required: ['confirm', 'window'],
      },
    });
  } catch (err) {
    return text(`Not filed: the desk could not ask for a confirmation (${err.message}).`);
  }
  if (answer?.action !== 'accept') return text(`Not filed: the person ${answer?.action === 'decline' ? 'declined' : 'did not answer'}.`);
  if (answer.content?.confirm !== true) return text('Not filed: the person did not tick "File this change request".');
  ticket += 1;
  return text(`Filed CHG-2026-0${ticket} on ${asset}: ${change}. Window: ${answer.content.window}. Status: waiting for the plant supervisor.`);
}

async function summarise(args) {
  const lines = LOG[args?.asset];
  if (!lines) return text(`Unknown asset "${args?.asset}". The desk knows: ${assets.join(', ')}.`, true);
  try {
    const r = await ask('sampling/createMessage', {
      messages: [{ role: 'user', content: { type: 'text', text: `Summarise this change log of ${args.asset} in three sentences for a shift supervisor. Keep every ticket number.\n\n${lines.join('\n')}` } }],
      systemPrompt: 'You summarise plant change logs. Use only what the log says.',
      maxTokens: 400,
    });
    const said = r?.content?.type === 'text' ? r.content.text : '';
    return text(`Summary (written by the host's model, ${r?.model ?? 'unnamed'}):\n${said}`);
  } catch (err) {
    return text(`The host did not write a summary: ${err.message}\nThe log as it is:\n${lines.join('\n')}`);
  }
}

async function handle(msg) {
  if (msg.id !== undefined && !msg.method) {
    const w = waiting.get(msg.id);
    if (!w) return;
    waiting.delete(msg.id);
    if (msg.error) w.reject(new Error(msg.error.message ?? 'refused')); else w.resolve(msg.result);
    return;
  }
  const { id, method, params } = msg;
  if (id === undefined) return; // notifications (initialized, cancelled …)
  try {
    if (method === 'initialize') {
      return send({ id, result: { protocolVersion: params?.protocolVersion ?? '2025-06-18', capabilities: { tools: {} }, serverInfo: { name: 'meridian-change-desk', version: '1.0.0' } } });
    }
    if (method === 'ping') return send({ id, result: {} });
    if (method === 'tools/list') return send({ id, result: { tools: TOOLS } });
    if (method === 'tools/call') {
      const name = params?.name;
      const result = name === 'request_change' ? await requestChange(params.arguments)
        : name === 'summarise_change_log' ? await summarise(params.arguments)
        : text(`No tool named ${name}.`, true);
      return send({ id, result });
    }
    send({ id, error: { code: -32601, message: `Method not found: ${method}` } });
  } catch (err) {
    send({ id, error: { code: -32603, message: err instanceof Error ? err.message : String(err) } });
  }
}

const rl = createInterface({ input: process.stdin });
rl.on('line', (line) => {
  if (!line.trim()) return;
  let msg;
  try { msg = JSON.parse(line); } catch { return; }
  handle(msg).catch((err) => process.stderr.write(`change-desk: ${err?.message ?? err}\n`));
});
rl.on('close', () => process.exit(0));
