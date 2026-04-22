module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  rootDir: '.',
  roots: ['<rootDir>/tests'],
  setupFiles: ['<rootDir>/tests/setup/env.ts'],
  testMatch: ['**/integration/**/*.test.ts'],
  clearMocks: true,
  restoreMocks: true,
  testTimeout: 30000,
  moduleFileExtensions: ['ts', 'js', 'json'],
  transform: {
    '^.+\\.ts$': ['ts-jest', { tsconfig: '<rootDir>/tsconfig.jest.json' }],
  },
};
