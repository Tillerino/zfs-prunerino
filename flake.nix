{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };
  outputs = {self, nixpkgs, ...}@inputs: let
    forAllSys = nixpkgs.lib.genAttrs nixpkgs.lib.platforms.all;
  in {
    packages = forAllSys (system: let
      pkgs = import nixpkgs { inherit system; };
      zfs-prunerino = pkgs.python3Packages.buildPythonPackage {
        name = "zfs-prunerino";
        src = ./.;

        installPhase = ''
          mkdir -p $out/bin
          cp -r $src/zfs-prunerino $out/bin
        '';
      };
    in {
      default = zfs-prunerino;
    });
  };
}
