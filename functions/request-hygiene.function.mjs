/**
 * The demo pack's worked hook (docs/enterprise/pack-extensions.md, slice 1): an `annotate` hook on
 * `access.requested`. Core calls it with the request as data and shows what it returns on the
 * request's row in the Approvals inbox, attributed to this pack. It sees only the payload — no
 * database, no audit log — and returns a score plus a line of text; core never interprets them.
 *
 * The score is deliberately simple: a request with no reason scores high (an admin should ask why),
 * a request with a sentence or two scores low. The risk pack replaces this with real signals.
 */
export default {
  name: 'request-hygiene',
  description: 'Annotates an access request with a hygiene score from the reason the person gave (demo hook; not a tool for agents).',
  parameters: {
    reason: { type: 'string', description: 'The reason the person gave', required: false },
    resourceKind: { type: 'string', description: 'What was asked for', required: false },
    resourceName: { type: 'string', description: 'Its name', required: false },
  },
  execute: async ({ reason, resourceKind, resourceName }) => {
    const words = String(reason ?? '').trim().split(/\s+/).filter(Boolean).length;
    const score = words === 0 ? 80 : words < 4 ? 50 : 15;
    const detail = words === 0 ? 'no reason was given' : `${words} word${words === 1 ? '' : 's'} of reason`;
    return JSON.stringify({
      hygiene: { kind: 'score', value: score, label: 'Hygiene', detail: [detail, `asked for ${resourceKind} "${resourceName}"`] },
      note: { kind: 'text', label: 'Demo hook', text: words === 0 ? 'Ask what this is for before granting.' : 'A reason was given; decide on its merits.' },
    });
  },
};
