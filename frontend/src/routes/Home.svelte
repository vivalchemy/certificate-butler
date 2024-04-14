<script lang="ts">
  import * as Tabs from "$lib/components/ui/tabs/index.js";
  import Form from "$lib/components/form/Form.svelte";
  import History from "$lib/components/history/History.svelte";
</script>

<div class="min-h-screen bg-slate-950 text-white">
  <Tabs.Root
    value="generate"
    class="flex flex-col items-center justify-center pt-8 pb-16"
  >
    <Tabs.List class="grid grid-cols-2 w-1/2 bg-slate-900">
      <Tabs.Trigger
        value="generate"
        class="data-[state=active]:bg-slate-700 data-[state=active]:text-white "
        >Generate</Tabs.Trigger
      >
      <Tabs.Trigger
        value="history"
        class="data-[state=active]:bg-slate-700 data-[state=active]:text-white "
        >History</Tabs.Trigger
      >
    </Tabs.List>
    <Tabs.Content value="generate">
      <Form />
    </Tabs.Content>
    <Tabs.Content value="history">
      <History />
    </Tabs.Content>
  </Tabs.Root>
</div>
