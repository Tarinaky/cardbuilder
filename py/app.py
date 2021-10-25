import argparse
import pathlib

from inscryption_card_builder import InscryptionCardBuilder

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Inscryption cards from CSV data")
    parser.add_argument('-r','--resource_path', help="Directory containing png templates", type=pathlib.Path, required=True)
    parser.add_argument('-i','--inputfile', help="Source CSV file to generate from", type=pathlib.Path, required=True)
    parser.add_argument('-o','--outdir', help="Directory to save resulting cards to", type=pathlib.Path, required=True)
    parser.add_argument('--card', help="Generate a specific card from the data", type=str)

    args = parser.parse_args()
    print("DEBUG: %s" % args)

    InscryptionCardBuilder(
        resources=args.resource_path,
        inputfile=args.inputfile,
    ).write(args.outdir, args)


