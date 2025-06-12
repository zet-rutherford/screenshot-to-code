import { useEffect, useRef } from "react";
import { generateCode } from "./generateCode";
import SettingsDialog from "./components/settings/SettingsDialog";
import { AppState, CodeGenerationParams, EditorTheme, Settings } from "./types";
import { IS_RUNNING_ON_CLOUD } from "./config";
import { PicoBadge } from "./components/messages/PicoBadge";
import { OnboardingNote } from "./components/messages/OnboardingNote";
import { usePersistedState } from "./hooks/usePersistedState";
import TermsOfServiceDialog from "./components/TermsOfServiceDialog";
import { USER_CLOSE_WEB_SOCKET_CODE } from "./constants";
import { extractHistory } from "./components/history/utils";
import toast from "react-hot-toast";
import { Stack } from "./lib/stacks";
import { CodeGenerationModel } from "./lib/models";
import useBrowserTabIndicator from "./hooks/useBrowserTabIndicator";
import { useAppStore } from "./store/app-store";
import { useProjectStore } from "./store/project-store";
import Sidebar from "./components/sidebar/Sidebar";
import PreviewPane from "./components/preview/PreviewPane";
import DeprecationMessage from "./components/messages/DeprecationMessage";
import { GenerationSettings } from "./components/settings/GenerationSettings";
import StartPane from "./components/start-pane/StartPane";
import { Commit } from "./components/commits/types";
import { createCommit } from "./components/commits/utils";
import GenerateFromText from "./components/generate-from-text/GenerateFromText";

function App() {
  const {
    // Inputs
    inputMode,
    setInputMode,
    isImportedFromCode,
    setIsImportedFromCode,
    referenceImages,
    setReferenceImages,
    initialPrompt,
    setInitialPrompt,

    head,
    commits,
    addCommit,
    removeCommit,
    setHead,
    appendCommitCode,
    setCommitCode,
    resetCommits,
    resetHead,
    updateVariantStatus,
    resizeVariants,

    // Outputs
    appendExecutionConsole,
    resetExecutionConsoles,
  } = useProjectStore();

  const {
    disableInSelectAndEditMode,
    setUpdateInstruction,
    appState,
    setAppState,
  } = useAppStore();

  // Settings
  const [settings, setSettings] = usePersistedState<Settings>(
    {
      openAiApiKey: null,
      openAiBaseURL: null,
      anthropicApiKey: null,
      screenshotOneApiKey: null,
      isImageGenerationEnabled: false,
      editorTheme: EditorTheme.COBALT,
      generatedCodeConfig: Stack.HTML_CSS,
      codeGenerationModel: CodeGenerationModel.CLAUDE_3_5_SONNET_2024_06_20,
      isTermOfServiceAccepted: false,
    },
    "setting"
  );

  const wsRef = useRef<WebSocket>(null);

  // Computed values
  const model = settings.codeGenerationModel || CodeGenerationModel.GPT_4_VISION;
  
  const showBetterModelMessage =
    model !== CodeGenerationModel.GPT_4O_2024_05_13 &&
    model !== CodeGenerationModel.CLAUDE_3_5_SONNET_2024_06_20 &&
    appState === AppState.INITIAL;

  const showSelectAndEditFeature =
    (model === CodeGenerationModel.GPT_4O_2024_05_13 ||
      model === CodeGenerationModel.CLAUDE_3_5_SONNET_2024_06_20) &&
    (settings.generatedCodeConfig === Stack.HTML_TAILWIND ||
      settings.generatedCodeConfig === Stack.HTML_CSS);

  // Hooks
  useBrowserTabIndicator(appState === AppState.CODING);

  // Effects
  useEffect(() => {
    if (!settings.generatedCodeConfig) {
      setSettings((prev) => ({
        ...prev,
        generatedCodeConfig: Stack.HTML_CSS,
      }));
    }
  }, [settings.generatedCodeConfig, setSettings]);

  // Functions
  const reset = () => {
    setAppState(AppState.INITIAL);
    setUpdateInstruction("");
    disableInSelectAndEditMode();
    resetExecutionConsoles();
    resetCommits();
    resetHead();
    setInputMode("image");
    setReferenceImages([]);
    setIsImportedFromCode(false);
  };

  const regenerate = () => {
    if (head === null) {
      toast.error("No current version set. Please contact support via chat or Github.");
      throw new Error("Regenerate called with no head");
    }

    const currentCommit = commits[head];
    if (currentCommit.type !== "ai_create") {
      toast.error("Only the first version can be regenerated.");
      return;
    }

    if (inputMode === "image" || inputMode === "video") {
      doCreate(referenceImages, inputMode);
    } else {
      doCreateFromText(initialPrompt);
    }
  };

  const cancelCodeGeneration = () => {
    wsRef.current?.close?.(USER_CLOSE_WEB_SOCKET_CODE);
  };

  const cancelCodeGenerationAndReset = (commit: Commit) => {
    if (commit.type === "ai_create") {
      reset();
    } else {
      removeCommit(commit.hash);
      const parentCommitHash = commit.parentHash;
      if (parentCommitHash) {
        setHead(parentCommitHash);
      } else {
        throw new Error("Parent commit not found");
      }
      setAppState(AppState.CODE_READY);
    }
  };

  function doGenerateCode(params: CodeGenerationParams) {
    resetExecutionConsoles();
    setAppState(AppState.CODING);

    const updatedParams = { ...params, ...settings };
    const baseCommitObject = {
      variants: Array(4).fill(null).map(() => ({ code: "" })),
    };

    const commitInputObject =
      params.generationType === "create"
        ? {
            ...baseCommitObject,
            type: "ai_create" as const,
            parentHash: null,
            inputs: { image_url: referenceImages[0] },
          }
        : {
            ...baseCommitObject,
            type: "ai_edit" as const,
            parentHash: head,
            inputs: {
              prompt: params.history ? params.history[params.history.length - 1] : "",
            },
          };

    const commit = createCommit(commitInputObject);
    addCommit(commit);
    setHead(commit.hash);

    generateCode(wsRef, updatedParams, {
      onChange: (token, variantIndex) => {
        appendCommitCode(commit.hash, variantIndex, token);
      },
      onSetCode: (code, variantIndex) => {
        setCommitCode(commit.hash, variantIndex, code);
      },
      onStatusUpdate: (line, variantIndex) => appendExecutionConsole(variantIndex, line),
      onVariantComplete: (variantIndex) => {
        console.log(`Variant ${variantIndex} complete event received`);
        updateVariantStatus(commit.hash, variantIndex, "complete");
      },
      onVariantError: (variantIndex, error) => {
        console.error(`Error in variant ${variantIndex}:`, error);
        updateVariantStatus(commit.hash, variantIndex, "error", error);
      },
      onVariantCount: (count) => {
        console.log(`Backend is using ${count} variants`);
        resizeVariants(commit.hash, count);
      },
      onCancel: () => {
        cancelCodeGenerationAndReset(commit);
      },
      onComplete: () => {
        setAppState(AppState.CODE_READY);
      },
    });
  }

  function doCreate(referenceImages: string[], inputMode: "image" | "video") {
    reset();
    setReferenceImages(referenceImages);
    setInputMode(inputMode);

    if (referenceImages.length > 0) {
      doGenerateCode({
        generationType: "create",
        image: referenceImages[0],
        inputMode,
      });
    }
  }

  function doCreateFromText(text: string) {
    reset();
    setInputMode("text");
    setInitialPrompt(text);
    doGenerateCode({
      generationType: "create",
      inputMode: "text",
      image: text,
    });
  }

  async function doUpdate(updateInstruction: string, selectedElement?: HTMLElement) {
    if (updateInstruction.trim() === "") {
      toast.error("Please include some instructions for AI on what to update.");
      return;
    }

    if (head === null) {
      toast.error("No current version set. Contact support or open a Github issue.");
      throw new Error("Update called with no head");
    }

    let historyTree;
    try {
      historyTree = extractHistory(head, commits);
    } catch {
      toast.error("Version history is invalid. This shouldn't happen. Please contact support or open a Github issue.");
      throw new Error("Invalid version history");
    }

    let modifiedUpdateInstruction = updateInstruction;

    if (selectedElement) {
      modifiedUpdateInstruction =
        updateInstruction +
        " referring to this element specifically: " +
        selectedElement.outerHTML;
    }

    const updatedHistory = [...historyTree, modifiedUpdateInstruction];

    doGenerateCode({
      generationType: "update",
      inputMode,
      image: inputMode === "text" ? initialPrompt : referenceImages[0],
      history: updatedHistory,
      isImportedFromCode,
    });

    setUpdateInstruction("");
  }

  const handleTermDialogOpenChange = (open: boolean) => {
    setSettings((s) => ({
      ...s,
      isTermOfServiceAccepted: !open,
    }));
  };

  return (
    <div className="mt-2 dark:bg-black dark:text-white">
      {/* Global Components */}
      {IS_RUNNING_ON_CLOUD && <PicoBadge />}
      {IS_RUNNING_ON_CLOUD && (
        <TermsOfServiceDialog
          open={!settings.isTermOfServiceAccepted}
          onOpenChange={handleTermDialogOpenChange}
        />
      )}

      {/* Sidebar */}
      <div className="lg:fixed lg:inset-y-0 lg:z-40 lg:flex lg:w-[32rem] lg:flex-col">
        <div className="flex grow flex-col gap-y-4 overflow-y-auto border-r border-gray-200 bg-white px-6 py-4 dark:bg-zinc-950 dark:text-white">
          
          {/* Header */}
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold">Auto Design</h1>
            <SettingsDialog settings={settings} setSettings={setSettings} />
          </div>

          {/* Generation Settings */}
          <GenerationSettings settings={settings} setSettings={setSettings} />

          {/* Status Messages */}
          {showBetterModelMessage && <DeprecationMessage />}
          {IS_RUNNING_ON_CLOUD && !settings.openAiApiKey && <OnboardingNote />}

          {/* Content based on App State */}
          {appState === AppState.INITIAL && (
            <GenerateFromText doCreateFromText={doCreateFromText} />
          )}

          {(appState === AppState.CODING || appState === AppState.CODE_READY) && (
            <Sidebar
              showSelectAndEditFeature={showSelectAndEditFeature}
              doUpdate={doUpdate}
              regenerate={regenerate}
              cancelCodeGeneration={cancelCodeGeneration}
            />
          )}
        </div>
      </div>

      {/* Main Content */}
      <main className="py-2 lg:pl-[32rem] w-full">
        {appState === AppState.INITIAL && (
          <StartPane doCreate={doCreate} />
        )}

        {(appState === AppState.CODING || appState === AppState.CODE_READY) && (
          <PreviewPane doUpdate={doUpdate} reset={reset} settings={settings} />
        )}
      </main>
    </div>
  );
}

export default App;