import { Selector, t } from "testcafe";

class AlbumPage {
  firstImage = Selector(".grid__group.item-slider").child(0);

  async selectFirstImage() {
    return t.click(this.firstImage);
  }
}

export default new AlbumPage();
