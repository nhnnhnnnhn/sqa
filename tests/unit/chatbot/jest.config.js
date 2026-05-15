const tsJest = require.resolve("ts-jest");

module.exports = {
  clearMocks: true,
  rootDir: "../../..",
  testEnvironment: "jsdom",
  testMatch: ["<rootDir>/tests/unit/chatbot/tests/**/*.test.ts?(x)"],
  setupFilesAfterEnv: ["<rootDir>/tests/unit/chatbot/jest.setup.ts"],
  collectCoverageFrom: [
    "<rootDir>/frontend_user/src/components/chat-mini/page.tsx"
  ],
  coverageDirectory: "<rootDir>/tests/unit/chatbot/coverage",
  coverageReporters: ["text", "html", "lcov"],
  moduleNameMapper: {
    "^react$": "<rootDir>/tests/unit/chatbot/node_modules/react",
    "^react/jsx-runtime$": "<rootDir>/tests/unit/chatbot/node_modules/react/jsx-runtime.js",
    "^react-dom$": "<rootDir>/tests/unit/chatbot/node_modules/react-dom",
    "\\.(css|less|scss|sass)$": "<rootDir>/tests/unit/chatbot/__mocks__/styleMock.js",
    "^react-markdown$": "<rootDir>/tests/unit/chatbot/__mocks__/react-markdown.tsx"
  },
  transform: {
    "^.+\\.(ts|tsx)$": [
      tsJest,
      {
        tsconfig: "<rootDir>/tests/unit/chatbot/tsconfig.json"
      }
    ]
  }
};
