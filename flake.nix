{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
  };
  outputs = {self, nixpkgs, ...}@inputs: let
    forAllSys = nixpkgs.lib.genAttrs nixpkgs.lib.platforms.all;
  in {
    packages = forAllSys (system: let
      pkgs = import nixpkgs { inherit system; };
      zfs-prunerino = with pkgs.python3Packages; buildPythonPackage {
        name = "zfs-prunerino";
        src = ./.;
        version = "0.1";
        meta = {
          description = "Simple tool to prune zfs snapshots with spaced retention";
          homepage = "https://github.com/Tillerino/zfs-prunerino";
          license = pkgs.lib.licenses.asl20;
        };
        format = "setuptools";
        buildsystem = [ setuptools wheel ];
      };
    in {
      default = zfs-prunerino;
    });
  };
}
