{ pkgs, ... }: {
  channel = "stable-24.05";

  packages = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.setuptools
    pkgs.python312Packages.wheel
    pkgs.python312Packages.flask
  ];

  idx = {
    extensions = [
      "ms-python.python"
      "rangav.vscode-thunder-client"
    ];

    workspace = {
      onCreate = {
        install = ''
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt
        '';
        default.openFiles = [
          "README.md"
          "src/index.html"
          "main.py"
        ];
      };

      onStart = {
        run-server = "./devserver.sh";
      };
    };
  };
}

