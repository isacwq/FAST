module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/base',
    'plugin:vue/essential',
    'plugin:vue/recommended',
    'plugin:vue/strongly-recommended',
    '@vue/standard'
  ],
  parserOptions: {
    parser: 'babel-eslint'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-restricted-imports': ['error', {
      patterns: [{
        group: ['.*', '..*'],
        message: 'Please use absolute imports with "@"'
      }]
    }],
    camelcase: [2, {
      properties: 'always'
    }],
    'vue/object-curly-spacing': ['error', 'always']
  }
}
