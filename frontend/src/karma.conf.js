module.exports = function (config) {
  config.set({
    // ... your other config settings
    browsers: ['Chrome', 'ChromiumHeadlessNoSandbox'],
    customLaunchers: {
      ChromiumHeadlessNoSandbox: {
        base: 'ChromiumHeadless',
        flags: ['--no-sandbox', '--disable-setuid-sandbox']
      }
    }
  });
};
