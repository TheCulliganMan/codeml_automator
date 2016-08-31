#!/usr/bin/env python
import argparse
import os
import subprocess as sp
import shutil
import codeml_builder


def build_paths(paths_list):
	new_paths = []
	for path in paths_list:
		if not os.path.isdir(path):
			os.makedirs(path)
		new_paths.append(os.path.abspath(path))
	return new_paths

def get_genes(gene_dir):
	genes = []
	for gene in os.listdir(gene_dir):
		if gene.endswith(".nuc"):
			gene_name = gene.split(".")[0]
			gene = os.path.join(gene_dir, gene)
			genes.append((gene, gene_name))
	return genes


def get_trees(tree_dir, full_tree):
	trees = []
	for tree in os.listdir(tree_dir):
		if tree.endswith(".trees"):
			if tree != full_tree:
				tree_name = tree.split(".")[0]
				tree_name = tree_name.split("_")[-1]
				tree = os.path.join(tree_dir, tree)
				trees.append((tree, tree_name))
	return trees

def make_new_output(ctr_folder, output_folder):
	new_path =  os.path.join(ctr_folder, output_folder)
	os.makedirs(new_path)
	return new_path


def run_gene_controls(gene_controls, genes, trees, paml_output, ctr_folder):

	output_files = []

	for gene_file, gene_name in genes:
		for tree_file, tree_name in trees:
			for ctl_function, f_name in gene_controls:

				output_name = "{}_{}_{}".format(gene_name,
												tree_name,
												f_name)


				mlc_out_file = os.path.join(paml_output,
											"{}.mlc".format(output_name))

				output_folder = make_new_output(ctr_folder, output_name)

				ctl_out_file = os.path.join(output_folder,
											"{}.ctl".format(output_name))

				ctl_output = ctl_function(gene_file, tree_file, mlc_out_file)

				with open(ctl_out_file, "w+") as output_handle:
					output_handle.write(ctl_output)

				output_files.append(output_folder)

	return output_files


def main():

	parser = argparse.ArgumentParser(description='Process some codeml files.')

	parser.add_argument('-gene_dir', default='nuc',
                        help='Location of the genes that you want to run. (default "nuc")')
	parser.add_argument('-tree_dir', default='tree',
                        help='location of your tree files. (default "tree")')
	parser.add_argument('-tree_file', default='treen.trees',
                        help='location of the master tree file. (default "<tree_dir>/treen.trees")')
	parser.add_argument('-paml_output', default='paml_output',
                        help='where to output the paml files. (default "paml_output")')
	parser.add_argument('-c', type=int, default=1,
                        help='Number of cores (default 1)')
	parser.add_argument('-new_controls_dir', default='new_controls',
						help='where more files are output. And codeml is run (default "new_controls")')

	args = parser.parse_args()
	gene_dir = args.gene_dir
	tree_dir = args.tree_dir
	full_tree = args.tree_file
	paml_output = args.paml_output
	output_folder = args.new_controls_dir
	cores = args.c

	paths_list = [gene_dir, tree_dir,
				  paml_output, output_folder]
	gene_dir, tree_dir, paml_output, output_folder = build_paths(paths_list)

	genes = get_genes(gene_dir)

	#For the first two models
	gene_controls = [(codeml_builder.format_control_bsm2, "BSM2"),
					 (codeml_builder.format_control_bsmo, "BSMO")]

	trees = get_trees(tree_dir, full_tree)
	control_dirs = run_gene_controls(gene_controls, genes, trees,
									 paml_output, output_folder)

	# For the second two models
	gene_controls = [(codeml_builder.format_control_mo_8, "MO_8"),
				     (codeml_builder.format_control_m1, "M1")]
	trees = [(os.path.join(tree_dir, full_tree), "tree")]
	control_dirs += run_gene_controls(gene_controls, genes, trees,
									  paml_output, output_folder)

	codeml_builder.run_codeml(control_dirs, c=cores)

if __name__ == "__main__":
	main()
