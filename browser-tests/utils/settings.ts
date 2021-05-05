class Settings {
  get baseUrl() {
    return this.getOrError("BROWSER_TESTING_BASE_URL");
  }

  private getOrError(variableName: string) {
    const variable = process.env[variableName];

    if (!variable) {
      throw Error(`Environment variable ${variableName} is missing`);
    }

    return variable;
  }
}

export default new Settings();
