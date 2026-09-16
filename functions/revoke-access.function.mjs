/**
 * revoke_access — the demo's "dangerous" action. The pack adds a tool-approval entry for it to
 * tools.yaml, so a person must approve before it runs. It performs no real revocation; it records
 * what would have happened.
 */
export default {
  name: 'revoke_access',
  description: 'Revoke every access of a person or contractor after a security incident (approval required)',
  parameters: {
    subject: { type: 'string', description: 'The person or contractor, by name or account' },
    reason: { type: 'string', description: 'The incident or reason' },
  },
  execute: async ({ subject, reason }) => {
    if (!subject) throw new Error('subject is required');
    return JSON.stringify({ revoked: subject, reason: reason ?? '', at: new Date().toISOString(), note: 'Demo function: no real access was changed.' });
  },
};
