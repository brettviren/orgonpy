;;; ox-onpy.el --- Python Back-End for Org Export Engine

;; Copyright (C) 2015 Brett Viren.

;; Author: Brett Viren

;; Comentary:
;; 
;; This is part of Orgonpy. https://github.com/brettviren/orgonpy

;; You can redistribute it and/or modify it under the terms of the GNU
;; General Public License as published by the Free Software
;; Foundation, either version 3 of the License, or (at your option)
;; any later version.  For a copy of the licence see
;; <http://www.gnu.org/licenses/>.

;; Because I don't know what I'm doing, this borrows heavily from ox-latex.el.

;;; Code:

(eval-when-compile (require 'cl))
(require 'ox)
(require 'ox-org)
;(require 'ox-publish)
(require 'org-json)

;;; Define Back-End

;(org-export-define-backend 'onpy
(org-export-define-derived-backend 'onpy 'org
  :filters-alist '((:filter-final-output . org-onpy-jsonify-parse-tree))
  :menu-entry
  '(?j "Export to JSON"
       ((?J "As JSON buffer" org-onpy-export-as-json)
	(?j "As JSON file" org-onpy-export-to-json))))

(defun org-onpy-jsonify-parse-tree (element contents info)
  "An org filter that returns the entire tree as JSON"
  (org-json-tree-to-json-string 
   (org-json-straigten-tree (plist-get info :parse-tree))))

;;;###autoload
(defun org-onpy-export-as-json
  (&optional async subtreep visible-only body-only ext-plist)
  "Export current buffer as a JSON buffer."
  (interactive)
  (message "org-onpy-export-as-json called")
  (org-export-to-buffer 'onpy "*Org JSON Export*"
    async subtreep visible-only body-only ext-plist (lambda () (javascript-mode))))
  
;;;###autoload
(defun org-onpy-export-to-json
  (&optional async subtreep visible-only body-only ext-plist)
  "Export current buffer to a JSON file."
  (interactive)
  (let ((outfile (org-export-output-file-name ".json" subtreep)))
    (org-export-to-file 'onpy outfile
      async subtreep visible-only body-only ext-plist)))

(provide 'ox-onpy)
