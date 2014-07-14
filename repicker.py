#!/usr/bin/python
import os, sys, re, shutil, subprocess


"""
Repicker
Version 0.2 - Tue 15 Jul 2014

Re-pick pictures in a new size based on the filenames of pictures in an input
directory.

Usage: repicker <input_picks> <source_images> <output_dir> <target_width>

by Reimund Trost <reimund@code7.se>
<http://lumens.se/>

"""

def main(argv=None):
	if argv is None:
		argv = sys.argv

	repicker = Repicker(argv)

class Repicker:

	def __init__(self, args):
		# Must have at least three arguments.
		if 3 > len(args):
			print('Expected at least 3 arguments.')
			print('Usage: repicker <input_picks> <input_new_files>  <output_dir> <target_width>')
			return False

		self.picks_dir        = args[1] + '/'
		self.src_dir          = args[2] + '/'
		self.out_dir          = args[3] + '/'
		self.diptych_dir_name = 'diptychs'
		self.target_width     = '920' if 3 < len(args) else args[4]

		if not os.path.isdir(self.picks_dir):
			print('Picks directory does not exist.')
			return

		if not os.path.isdir(self.src_dir):
			print('Source directory does not exist.')
			return

		if not os.path.isdir(self.out_dir):
			print('Output directory does not exist.')
			return

		if not os.path.isdir(self.out_dir + self.diptych_dir_name):
			os.mkdir(self.out_dir + self.diptych_dir_name)

		self.pick_source_images()


	def resolve_original_names(self, str):
		stripped_prefix = re.sub(r'^\d+_', '', str)
		order           = re.sub(r'_\d{8}_[a-z]{4}_(?:\d+(?:_bw)?_?)*\.jpg$', '', str)

		if None != re.search(r'(\d+_(?:bw_)?)+\d+(?:_bw)?\.jpg$', stripped_prefix):
			basename  = re.sub(r'(\d+(?:_bw)?_)*\d+(?:_bw)?\.jpg$', '', stripped_prefix)
			image_ids = re.search(r'(?:(\d+(?:_bw)?)_)*(\d+(?:_bw)?)\.jpg$', stripped_prefix).groups()

			original_names = []
			for x in image_ids:
				original_names.append(basename + x + '.jpg')

		else:
			original_names = [re.sub(r'^\d+_', '', str)]

		return (original_names, order)


	def pick_source_images(self):
		self.picks = get_images(self.picks_dir)

		for p in self.picks:
			original_names = self.resolve_original_names(p)
			dest           = self.out_dir

			if 1 < len(original_names[0]):
				self.tychify(original_names[0], p)

				dest = self.out_dir + self.diptych_dir_name + '/'
				prefix = ''
			else:
				prefi x = original_names[1] + '_'

			shutil.copy(self.src_dir + original_names[0][0], dest + prefix + original_names[0][0])

	def tychify(self, src, dest_name):
		paths    = []
		img_args = []

		for s in src:
			img_args.append(os.path.realpath(self.src_dir + s))

		args           = ['tychify', '-t'] + img_args + ['-s 3', '-x ' + self.target_width, '-d ' + self.out_dir]

		basename       = re.sub(r'(\d+(?:_bw)?_)*\d+(?:_bw)?\.jpg$', '', src[0])
		tp_output_name = basename + ('_'.join(src)).replace(basename, '').replace('.jpg', '') + '.jpg'

		if re.search(r'_bw', dest_name):
			tp_output_name = '_'.join(src).replace('.jpg', '') + '.jpg'

		subprocess.call(args)
		os.rename(self.out_dir + tp_output_name, self.out_dir + dest_name)

def get_images(path):
	images = []

	if (os.path.isdir(path)):
		dir_files = [x for x in os.listdir(path)]

		for file in dir_files:
			if file.endswith(('.jpg')):
				images.append(file)

	return images


if __name__ == "__main__":
    sys.exit(main())

