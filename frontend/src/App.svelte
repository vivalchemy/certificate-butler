<script>
  import { Router, Route } from "svelte-routing";
  import Home from "./routes/Home.svelte";
  import About from "./routes/About.svelte";
</script>

<Router url="">
  <Route path="/" component={Home} />
  <Route path="/about/" component={About} />
</Router>
