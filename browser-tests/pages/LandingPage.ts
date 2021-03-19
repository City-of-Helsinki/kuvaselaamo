import { Selector } from "testcafe";

class LandingPage {
  title = Selector("h1").withText(
    "Tervetuloa Helsinki-aiheisten valokuvien aarreaittaan!"
  );
}

export default new LandingPage();
