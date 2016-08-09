#!/usr/bin/env python

import os
import subprocess as sp 
import shutil
import ctl

gene_dir = "nuc"
tree_dir = "tree"
full_tree = "treen.trees"
paml_output = "paml_output"


def get_genes():
	genes = []
	for gene in os.listdir(gene_dir):
		if gene.endswith(".nuc"):
			gene_name = gene.split(".")[0]
			gene = "../../nuc/{}".format(gene)
			genes.append((gene, gene_name))
	return genes


def get_trees():
	trees = []
	for tree in os.listdir(tree_dir):
		if tree.endswith(".trees"):
			if tree != full_tree:
				tree_name = tree.split(".")[0]
				tree_name = tree_name.split("_")[-1]
				tree = "../../tree/{}".format(tree)
				trees.append((tree, tree_name))
	return trees


def run_gene_controls(gene_controls, genes, trees):
	
	output_files = []

	for gene_file, gene_name in genes:
		for tree_file, tree_name in trees:
			for ctl_function, f_name in gene_controls:

				output_name = "{}_{}_{}".format(gene_name, 
												tree_name, 
												f_name)

				output_folder = "new_controls/{}".format(output_name)
				
				if not os.path.isdir(output_folder):
					os.makedirs(output_folder)

				mlc_out_file = "../../paml_output/{}.mlc".format(output_name)
				ctl_out_file = "{}/{}.ctl".format(output_folder, output_name)

				ctl_output = ctl_function(gene_file, tree_file, mlc_out_file)

				with open(ctl_out_file, "w+") as output_handle:
					output_handle.write(ctl_output)

				output_files.append(output_folder)

	return output_files


def main():
	genes = get_genes()
	
	#For the first two models
	gene_controls = [(ctl.format_control_bsm2, "BSM2"), 
						 (ctl.format_control_bsmo, "BSMO")]
	trees = get_trees()
	control_dirs = run_gene_controls(gene_controls, genes, trees)

	# For the second two models
	gene_controls = [(ctl.format_control_mo_8, "MO_8"), 
				     (ctl.format_control_m1, "M1")]
	trees = [("../../tree/" + full_tree, "tree")]
	control_dirs += run_gene_controls(gene_controls, genes, trees)
	
	ctl.run_codeml(control_dirs)

if __name__ == "__main__":
	main()
	
