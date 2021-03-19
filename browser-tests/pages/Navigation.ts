import { Selector, t } from "testcafe";

class Navigation {
  albumLink = Selector("a").withText("Selaa albumeita");

  async goToAlbumList() {
    return t.click(this.albumLink);
  }
}

export default new Navigation();
