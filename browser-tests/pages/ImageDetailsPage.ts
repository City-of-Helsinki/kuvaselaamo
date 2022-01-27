import { Selector, t, ClientFunction } from "testcafe";

class ImageDetailsPage {
  mainImage = Selector(".image-viewer__image");
  title = Selector("h1").nth(8);
  creator = this.recordMeta("Creator");
  time = this.recordMeta("Date");
  feedbackForm = Selector("form#feedback-form");

  async hasMainImage() {
    return t.expect(this.mainImage.exists).ok();
  }

  recordMeta(title: string) {
    return Selector(".record-meta__paragraph").withText(`${title}:`);
  }
}

export default new ImageDetailsPage();
