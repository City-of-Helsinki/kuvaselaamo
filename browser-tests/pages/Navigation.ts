import { Selector, t } from "testcafe";

class Navigation {
  albumLink = Selector("a").withText("Explore albums");

  async goToAlbumList() {
    return t.click(this.albumLink);
  }
}

export default new Navigation();
