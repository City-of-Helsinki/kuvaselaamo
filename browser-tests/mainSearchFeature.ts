import * as RouteUtils from "./utils/route";
import landingPage from "./pages/LandingPage";
import searchPage from "./pages/SearchPage";
import imageDetailsPage from "./pages/ImageDetailsPage";

fixture`Main search fucntionality`.page(RouteUtils.getRoute("/"));

test("As a user I want to be able to use the main search functionality to find images", async (t) => {
  await landingPage.search("Sederholmin talo");
  await searchPage.selectResult("Sederholmin talo");

  await t.expect(imageDetailsPage.title.innerText).eql("Sederholmin talo");
});
