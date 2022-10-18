import * as RouteUtils from "./utils/route";
import imageDetailsPage from "./pages/ImageDetailsPage";

fixture`Image feature`.page(
  RouteUtils.getImageRoute("hkm.7151C8C3-13C1-4F31-851B-0502AA5BB390")
);

test("As a user I want to be able to see details of images", async (t) => {
  await imageDetailsPage.hasMainImage();
  await t.expect(imageDetailsPage.creator.exists).ok();
  await t.expect(imageDetailsPage.time.exists).ok();
  //await t.expect(imageDetailsPage.feedbackForm.exists).ok();
});
