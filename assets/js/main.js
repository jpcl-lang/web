/* Theme toggle.

   The CSS already renders both themes on its own: dark by default, light when
   the reader's system asks for it. All this adds is an override, remembered
   between visits, which the inline script in <head> re-applies before the first
   paint so a chosen theme never flashes the other one.

   The button is hidden in the markup and revealed here, so a browser running
   without JavaScript never shows a control that cannot do anything. */

(() => {
    const KEY = "jpml-theme";
    const root = document.documentElement;
    const button = document.getElementById("theme-toggle");
    if (!button) return;

    const systemDark = window.matchMedia("(prefers-color-scheme: dark)");

    const current = () => root.dataset.theme || (systemDark.matches ? "dark" : "light");

    /* The address bar should follow the page. The markup ships two theme-color
       tags gated on the system preference; once a theme is chosen those gates
       point the wrong way, so drop them and state the colour outright. */
    const paintChrome = (theme) => {
        const colour = theme === "dark" ? "#192236" : "#fbfaf5";
        for (const tag of document.querySelectorAll('meta[name="theme-color"]')) {
            tag.removeAttribute("media");
            tag.content = colour;
        }
    };

    const describe = (theme) => {
        const next = theme === "dark" ? "light" : "dark";
        button.setAttribute("aria-label", `Switch to ${next} mode`);
        button.title = `Switch to ${next} mode`;
    };

    const apply = (theme) => {
        root.dataset.theme = theme;
        describe(theme);
        paintChrome(theme);
        try {
            localStorage.setItem(KEY, theme);
        } catch {
            /* storage blocked: the choice lasts for this page only */
        }
    };

    button.hidden = false;
    describe(current());

    button.addEventListener("click", () => {
        apply(current() === "dark" ? "light" : "dark");
    });

    /* With no override stored, keep following the system as it changes. */
    systemDark.addEventListener("change", () => {
        let stored = null;
        try {
            stored = localStorage.getItem(KEY);
        } catch {
            /* nothing stored that we can read */
        }
        if (stored !== "light" && stored !== "dark") describe(current());
    });
})();

/* Copy buttons. Also hidden in the markup, so a browser without the clipboard
   API never shows a button that cannot work. */

(() => {
    const clipboard = navigator.clipboard;
    if (!clipboard || typeof clipboard.writeText !== "function") return;

    for (const button of document.querySelectorAll(".copy")) {
        const block = button.closest(".code, .install");
        const source = block && (block.querySelector("pre code") || block.querySelector("code"));
        if (!source) continue;

        const label = block.classList.contains("install")
            ? "the install command"
            : (block.querySelector(".name")?.textContent.trim() || "the code");

        button.hidden = false;
        button.setAttribute("aria-label", `Copy ${label}`);

        button.addEventListener("click", async () => {
            try {
                await clipboard.writeText(source.innerText.trimEnd());
            } catch {
                return; /* permission refused: leave the button as it was */
            }

            button.textContent = "Copied";
            button.dataset.copied = "";

            clearTimeout(button.timer);
            button.timer = setTimeout(() => {
                button.textContent = "Copy";
                delete button.dataset.copied;
            }, 1600);
        });
    }
})();
