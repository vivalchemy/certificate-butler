<script lang="ts">
  import Counter from "$lib/components/ui/Counter.svelte";
  import type { Certificate } from "$lib/types";

  let url = "http://localhost:8000/api/certificate-template/";

  let previousCertificates: Certificate[];
  async function getData() {
    try {
      console.log("trying");
      await fetch(url)
        .then((res) => res.json())
        .then((data) => {
          previousCertificates = data;
          console.log(data);
          return data;
        });
    } catch (error) {
      console.log(error);
    }

    return previousCertificates;
  }
</script>

<h1 class="text-blue-500 text-6xl">This</h1>
is home
<a href="/about">Go to about</a>

<Counter />

{#await getData()}
  <p>Wait the data is being fetched</p>
  <!-- promise is pending -->
{:then value}
  <pre>{JSON.stringify(value, null, 2)}</pre>
  <!-- promise was fulfilled -->
  <div class="grid lg:grid-cols-4 md:grid-cols-3 sm:grid-cols-1"></div>
  {#each value as certificate}
    <div
      class="bg-slate-950 text-white flex flex-col gap-2 col-span-1 items-center justify-center max-w-[400px] max-h-[500px]"
    >
      <img
        src={certificate.image}
        alt={certificate.competitionName}
        class="w-[300px] h-[300px]"
      />
      <p>{certificate.competitionName}</p>
      <a href={certificate.csv} class="px-4 py-2 bg-blue-500">Download CSV</a>
    </div>
  {/each}
{:catch error}
  <p style="color: red">{error.message}</p>
  <!-- promise was fulfilled -->
{/await}
