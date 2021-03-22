import { Selector, t } from "testcafe";

class SearchPage {
  getResult(resultTitle: string) {
    return Selector(`img[alt="${resultTitle}"]`);
  }

  async selectResult(resultTitle: string) {
    await t.click(this.getResult(resultTitle));
  }
}

export default new SearchPage();
