<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:param name="use.id.as.filename" select="1" />
	<xsl:param name="html.stylesheet" select="'css/file-specification.css'" />

	<xsl:template name="tr.attributes">
		<xsl:param name="row" select="." />
		<xsl:param name="rownum" select="0" />

		<xsl:if test="$rownum mod 2 = 0">
			<xsl:attribute name="class">odd</xsl:attribute>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>
