<script lang="ts">
  import Input from "$lib/components/ui/input/input.svelte";
  import Label from "$lib/components/ui/label/label.svelte";
  import Button from "../ui/button/button.svelte";
  import * as Dialog from "$lib/components/ui/dialog/index.js";

  let API_URL = "http://localhost:8000/api/";
  let DJANGO_PORT = "http://localhost:8000";
  let certificatesUrl = API_URL + "certificate-templates/";
  let zipUrl = API_URL + "zipped-images";
  let competitionName: string;
  let fontSize: number;
  let fontFamily: string;
  let textPosition: number;
  let image: FileList;
  let csv: FileList;
  let files: FileList;
  let code: string;

  $: if (image && csv) {
    console.log(image);
    console.log(csv);

    for (const file of image) {
      console.log(`${file.name}: ${file.size} bytes`);
    }

    for (const file of csv) {
      console.log(`${file.name}: ${file.size} bytes`);
    }
  }

  // async function checkData() {
  //   // const formData = new FormData();
  //   // formData.append("competitionName", competitionName);
  //   // formData.append("fontSize", fontSize.toString());
  //   // formData.append("fontFamily", fontFamily);
  //   // formData.append("textPosition", textPosition.toString());
  //
  //   console.log("start");
  //   console.log(image)
  //   console.log(csv)
  //   console.log("end");
  //   // console.log(document.querySelector('input[type="file"]').files);
  // }
  async function postData() {
    const formData = new FormData();
    formData.append("competitionName", competitionName);
    formData.append("fontSize", fontSize.toString());
    formData.append("fontFamily", fontFamily);
    formData.append("textPosition", textPosition.toString());
    formData.append("image", image[0]);
    formData.append("csv", csv[0]);

    console.log(formData);
    const res = await fetch(certificatesUrl, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    console.log(data);
    code = data.code;
  }

  async function getZip() {
    const res = await fetch(zipUrl + `?id=${code}`);
    const data = await res.json();
    console.log(data);
    return data.data;
  }
</script>

<form
  class="grid md:grid-cols-2 w-screen gap-4 sm:grid-cols-1 text-white p-8 place-items-center"
  on:submit|preventDefault={postData}
>
  <div class="grid grid-cols-2 gap-2">
    <Label for="competitionName">Competition Name</Label>
    <Input
      type="text"
      name="competitionName"
      id="competitionName"
      bind:value={competitionName}
      class="bg-[rgba(255,255,255,0.1)]"
    />
    <Label for="fontSize">Font Size</Label>
    <Input
      type="number"
      name="fontSize"
      id="fontSize"
      bind:value={fontSize}
      class="bg-[rgba(255,255,255,0.1)]"
    />
    <Label for="fontFamily">Font Family</Label>
    <Input
      type="text"
      name="fontFamily"
      id="fontFamily"
      bind:value={fontFamily}
      class="bg-[rgba(255,255,255,0.1)]"
    />
    <Label for="textPosition">Text Position</Label>
    <Input
      type="number"
      name="textPosition"
      id="textPosition"
      bind:value={textPosition}
      class="bg-[rgba(255,255,255,0.1)]"
    />
  </div>
  <div class="flex flex-col gap-8">
    <input type="file" name="image" id="image" bind:files={image} />
    <input type="file" name="csv" id="csv" bind:files={csv} />
  </div>

  <div class="col-span-2 flex justify-center">
    <Button type="submit" class="px-12 py-8 text-xl rounded-lg">Generate</Button
    >
  </div>
</form>

{#if code}
  {#await getZip() then data}
    <Dialog.Root open={true}>
      <Dialog.Content class="sm:max-w-[425px] bg-black text-white">
        <Dialog.Header>
          <Dialog.Title>Download the Certificates</Dialog.Title>
        </Dialog.Header>
        <div class="flex flex-col">
          {#each data as zipFile}
            <a href={DJANGO_PORT + zipFile.href} download>{zipFile.code}</a>
          {/each}
        </div>
      </Dialog.Content>
    </Dialog.Root>
  {/await}
  <!-- {(code = "")} -->
{/if}
