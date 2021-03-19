import * as RouteUtils from "./utils/route";
import landingPage from "./pages/LandingPage";

fixture`Smoke test`.page(RouteUtils.getRoute("/"));

test("As a developer I want to know that the application is accessible after changes", async (t) => {
  await t.expect(landingPage.title.exists).ok();
});
