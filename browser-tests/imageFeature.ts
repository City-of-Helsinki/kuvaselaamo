import * as RouteUtils from "./utils/route";
import imageDetailsPage from "./pages/ImageDetailsPage";

fixture`Image feature`.page(
  RouteUtils.getImageRoute("hkm.HKMS000005:km0000oh6r")
);

test("As a user I want to be able to see details of images", async (t) => {
  await imageDetailsPage.hasMainImage();
  await t.expect(imageDetailsPage.creator.exists).ok();
  await t.expect(imageDetailsPage.time.exists).ok();
  //await t.expect(imageDetailsPage.feedbackForm.exists).ok();
});
