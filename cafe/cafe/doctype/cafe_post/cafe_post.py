# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import re

from frappe.model.document import Document
from frappe.utils import strip_html


class CafePost(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from cafe.cafe.doctype.cafe_post_tag_item.cafe_post_tag_item import (
			CafePostTagItem,
		)

		content: DF.TextEditor
		cover_image: DF.AttachImage | None
		description: DF.SmallText
		publication: DF.Link | None
		reading_time: DF.Data | None
		slug: DF.Data | None
		tags: DF.TableMultiSelect[CafePostTagItem]
		title: DF.Data
	# end: auto-generated types

	def before_save(self):
		if self.content:
			self.reading_time = self.calculate_reading_time()

		self.slug = self.generate_slug()

	def generate_slug(self) -> str:
		slug = self.title.lower()
		slug = re.sub(r"[^a-z0-9\s-]", "", slug)
		slug = re.sub(r"\s+", "-", slug).strip("-")
		slug = slug[:50].rstrip("-")

		return f"{slug}-{self.name}"

	def calculate_reading_time(self) -> str:
		WORDS_PER_MINUTE = 250

		text = strip_html(self.content or "")

		word_count = len(text.split())
		minutes = max(1, round(word_count / WORDS_PER_MINUTE))

		return f"{minutes} min read"
