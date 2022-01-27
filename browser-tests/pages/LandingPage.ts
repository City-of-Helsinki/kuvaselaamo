import { Selector, t } from "testcafe";

class LandingPage {
  title = Selector("h1").withText(
    "Welcome to the treasure trove of Helsinki-themed pictures"
  );
  searchInput = Selector("input#search");

  async search(searchTerm: string) {
    await t.typeText(this.searchInput, searchTerm).pressKey("enter");
  }
}

export default new LandingPage();
