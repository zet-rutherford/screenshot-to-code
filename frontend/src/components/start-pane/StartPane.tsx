import React from "react";
import ImageUpload from "../ImageUpload";
// import { UrlInputSection } from "../UrlInputSection";
// import ImportCodeSection from "../ImportCodeSection";
// import { Settings } from "../../types";
// import { Stack } from "../../lib/stacks";

interface Props {
  doCreate: (images: string[], inputMode: "image" | "video") => void;
}

const StartPane: React.FC<Props> = ({ doCreate}) => {
  return (
    <div className="flex flex-col justify-center items-center gap-y-10">
      <ImageUpload setReferenceImages={doCreate} />
      {/* <UrlInputSection
        doCreate={doCreate}
        screenshotOneApiKey={settings.screenshotOneApiKey}
      />
      <ImportCodeSection importFromCode={importFromCode} /> */}
    </div>
  );
};

export default StartPane;
