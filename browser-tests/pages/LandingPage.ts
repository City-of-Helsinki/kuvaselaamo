import { Selector, t } from "testcafe";

class LandingPage {
  title = Selector("h1").withText(
    "Tervetuloa Helsinki-aiheisten valokuvien aarreaittaan!"
  );
  searchInput = Selector("input#search");

  async search(searchTerm: string) {
    await t.typeText(this.searchInput, searchTerm).pressKey("enter");
  }
}

export default new LandingPage();
