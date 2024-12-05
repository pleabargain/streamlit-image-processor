import os

# Keep only sample1.jpg, sample2.jpg, and sample3.jpg
keep_files = {'sample1.jpg', 'sample2.jpg', 'sample3.jpg'}
sample_dir = 'sample_images'

for filename in os.listdir(sample_dir):
    if filename not in keep_files:
        try:
            os.remove(os.path.join(sample_dir, filename))
        except Exception as e:
            print(f"Error removing {filename}: {e}")
