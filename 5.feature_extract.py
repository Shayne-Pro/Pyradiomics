"""Extract 2D PNG radiomics features from explicitly matched image/mask pairs."""
import argparse
from pathlib import Path


def pair_files(image_dir, mask_dir):
    images = {p.name[:-len('_img.png')]: p for p in Path(image_dir).glob('*_img.png')}
    masks = {p.name[:-len('_mask.png')]: p for p in Path(mask_dir).glob('*_mask.png')}
    if not images:
        raise ValueError('No *_img.png files found in the image directory.')
    if images.keys() != masks.keys():
        raise ValueError(
            f'Unmatched case IDs: missing masks={sorted(images.keys() - masks.keys())}; '
            f'missing images={sorted(masks.keys() - images.keys())}'
        )
    return [(case_id, images[case_id], masks[case_id]) for case_id in sorted(images)]


def extract_features(pairs, class_label, mask_label):
    import numpy as np
    import SimpleITK as sitk
    from PIL import Image
    from radiomics.featureextractor import RadiomicsFeatureExtractor
    extractor = RadiomicsFeatureExtractor(force2D=True)
    rows = []
    for case_id, image_path, mask_path in pairs:
        with Image.open(image_path) as source:
            image = np.asarray(source.convert('L'))
        with Image.open(mask_path) as source:
            mask = np.asarray(source)
        if mask.ndim != 2 or image.shape != mask.shape:
            raise ValueError(f'{case_id}: mask must be single-channel and match the image dimensions.')
        if not np.any(mask == mask_label):
            raise ValueError(f'{case_id}: mask does not contain label {mask_label}.')
        result = extractor.execute(sitk.GetImageFromArray(image), sitk.GetImageFromArray(mask), label=mask_label)
        rows.append({'case_id': case_id, 'label': class_label, **result})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--images', type=Path, required=True, help='Directory of CASE_img.png images.')
    parser.add_argument('--masks', type=Path, required=True, help='Directory of CASE_mask.png masks.')
    parser.add_argument('--class-label', type=int, choices=(0, 1), required=True, help='Batch target: 0=normal, 1=abnormal.')
    parser.add_argument('--mask-label', type=int, default=255, help='Foreground value in the segmentation mask.')
    parser.add_argument('--output', type=Path, default=Path('features.xlsx'), help='Output .csv or .xlsx file.')
    args = parser.parse_args()
    if not args.images.is_dir() or not args.masks.is_dir():
        parser.error('--images and --masks must be existing directories.')
    if args.output.suffix.lower() not in ('.csv', '.xlsx'):
        parser.error('--output must end in .csv or .xlsx.')
    try:
        pairs = pair_files(args.images, args.masks)
    except ValueError as error:
        parser.error(str(error))
    if args.output.exists():
        parser.error(f'Output already exists: {args.output}. Choose another path.')
    rows = extract_features(pairs, args.class_label, args.mask_label)
    import pandas as pd
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    if args.output.suffix.lower() == '.csv':
        frame.to_csv(args.output, index=False)
    else:
        frame.to_excel(args.output, index=False)
    print(f'Extracted {len(rows)} cases to {args.output}')


if __name__ == '__main__':
    main()
