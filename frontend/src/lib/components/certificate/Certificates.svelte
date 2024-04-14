<script lang="ts">
  import { onMount } from "svelte";
  import * as Card from "$lib/components/ui/card/index.js";
  import Input from "$lib/components/ui/input/input.svelte";
  import Button from "../ui/button/button.svelte";
  import type { Certificate } from "$lib/types";
  let API_URL = "http://localhost:8000/api/";
  let certificatesUrl = API_URL + "certificate-templates";
  let previousCertificates: Certificate[];
  let search: string = "";
  let DJANGO_PORT = "http://localhost:8000";
  let zipUrl = API_URL + "zipped-images";

  onMount(() => {
    getData();
  });

  async function getData() {
    try {
      await fetch(certificatesUrl)
        .then((res) => res.json())
        .then((data) => {
          previousCertificates = data;
          // console.log(data);
          return data;
        });
    } catch (error) {
      console.log(error);
    }
    return previousCertificates;
  }

  async function getZip(code: string) {
    const res = await fetch(zipUrl + `?id=${code}`);
    const data = await res.json();
    console.log(data);
    return data.data;
  }
</script>

<!-- {console.log(typeof(previousCertificates))} -->
<div class="w-screen flex justify-end px-4 py-2">
  <Input
    bind:value={search}
    name="search"
    placeholder="Search"
    class="w-1/3 bg-[rgba(255,255,255,0.1)]"
  ></Input>
</div>
<div class="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-6 pt-8">
  <!-- {JSON.stringify(previousCertificates, null, 2)} -->
  {#await getData() then certificates}
    {#each certificates as certificate}
      {#if certificate.competitionName
        .toLowerCase()
        .includes(search.toLowerCase()) || search == ""}
        <Card.Root
          id={certificate.code}
          class="p-2 pt-2 bg-[rgba(255,255,255,0.1)] text-white border-none"
        >
          <Card.Content class="p-0">
            <img
              src={certificate.image}
              alt=""
              class="w-[320px] h-[240px] bg-cover bg-center rounded-lg p-1"
            />
          </Card.Content>
          <Card.Footer class="flex justify-between px-2 py-2"
            >{certificate.competitionName}</Card.Footer
          >
          {#await getZip(certificate.code) then data}
            {#each data as zipFile}
              <a href={DJANGO_PORT + zipFile.href} download>
                <Button class="w-full">Download Certificates</Button>
              </a>
            {/each}
          {/await}
        </Card.Root>
      {/if}
    {/each}
  {/await}
</div>
