SUBDIRS		= icons mime ui

dictdir		= $(datadir)/revelation
dict_DATA	= pwdict.hwm pwdict.pwd pwdict.pwi

desktopdir	= $(datadir)/applications
desktop_DATA	= revelation.desktop

schemadir	= @GCONF_SCHEMA_FILE_DIR@
schema_DATA	= revelation.schemas


pwdict.hwm pwdict.pwd pwdict.pwi: pwdict
	$(CRACK_MKDICT) pwdict | $(CRACK_PACKER) pwdict

install-data-hook:
	GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) \
	$(GCONFTOOL) --makefile-install-rule $(schema_DATA)

if FDO_MIME
	if test -z "$(DESTDIR)"; then \
		$(UPDATE_DESKTOP_DATABASE); \
	fi
endif

