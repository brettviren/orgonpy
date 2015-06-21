;; Fixme: need to not hard code this!
;(add-to-list 'load-path "~/.emacs.d/elpa/org-20150119")
(load "~/org-pub/pelican/bootorg.el")

(require 'org)
(require 'org-element)
(require 'json)

(defun straigten-tree (tree)
  "Null out circular references in the org-element TREE"
  (org-element-map tree (append org-element-all-elements
				org-element-all-objects '(plain-text))

    ;; the crux of this is to nullify references that turn the tree
    ;; into a Circular Object which the json module can't handle
    (lambda (x) 
      ;; guaranteed circluar
      (if (org-element-property :parent x)
	  (org-element-put-property x :parent "none"))
      ;; maybe circular if multiple structures accidently identical
      (if (org-element-property :structure x)
	  (org-element-put-property x :structure "none"))
      ))
  tree)

(defun org2jsonfile (infile outfile)
  (progn
    (save-excursion
      (find-file infile)
      (let* ((tree (org-element-parse-buffer 'object nil))
;	     (md (org-export-as 'gfm nil nil t))
	     (html (org-export-as 'html nil nil t)))
	(with-temp-file outfile
	  (insert (json-encode 
		   (list
		    :html html
;		    :markdown md
		    :tree (straigten-tree tree)))))))))

;(org2jsonfile "/opt/bv/projects/pelican-blog/orgonpy/tests/samples/blog.org" 
;	      "/tmp/blog.json" )
;(org2jsonfile "/home/bv/org-pub/topics/waf/index.org" "/tmp/foo.json")
