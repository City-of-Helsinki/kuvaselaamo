import * as RouteUtils from "./utils/route";
import navigation from "./pages/Navigation";
import imageDetailsPage from "./pages/ImageDetailsPage";
import albumListPage from "./pages/AlbumListPage";
import albumPage from "./pages/AlbumPage";

fixture`Album feature`.page(RouteUtils.getRoute("/"));

test("As a user I want to be able to find images through albums", async () => {
  await navigation.goToAlbumList();
  await albumListPage.selectFirstCollection();
  await albumPage.selectFirstImage();

  await imageDetailsPage.hasMainImage();
});
