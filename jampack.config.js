// Optional optimization profile. Run in a separate CI job after compatibility checks.
// It optimizes generated output only; it does not change the static source architecture.
export default {
  criticalCSS: { inline: true },
  compress: true,
  prefetch: true
};
