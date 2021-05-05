import { Selector, t } from "testcafe";

class AlbumListPage {
  firstAlbum = Selector(".public-collections__wrapper").child(0);

  async selectFirstCollection() {
    return t.click(this.firstAlbum);
  }
}

export default new AlbumListPage();
