MODULES = growroot rescuevol overlayroot dyn-netconf copymods rooturl updateroot
INITRAMFS_D = /usr/share/initramfs-tools
IRD = $(DESTDIR)/$(INITRAMFS_D)
DRACUT_D = /usr/lib/dracut
ULIB_PRE = $(DESTDIR)/usr/lib/cloud-initramfs-

build:

install:
	mkdir -p "$(IRD)/hooks" "$(IRD)/scripts" "$(DESTDIR)/etc"
	set -e; for d in $(MODULES); do \
		[ -d "$$d/hooks" ] || continue ; \
		install "$$d/hooks"/* "$(IRD)/hooks" ; \
		done
	set -e ; for d in $(MODULES); do \
		for sd in $$d/scripts/*; do \
			[ -d $$sd ] || continue; \
			td="$(IRD)/scripts/$${sd##*/}"; \
			mkdir -p "$$td" ; \
			install "$$sd"/* "$$td"; \
		done; done
	set -e ; for d in $(MODULES); do \
		[ -d $$d/conf-hooks.d/ ] || continue; \
		mkdir -p "$(IRD)/conf-hooks.d"; \
		install -m 644 "$$d/conf-hooks.d"/* "$(IRD)/conf-hooks.d/" ; \
		done
	set -e; for d in $(MODULES); do \
		[ -d "$$d/etc" ] || continue ; \
		for f in $$d/etc/*; do \
		    if [ -d "$$f" ];then \
		    		install -m 755 -d "$(DESTDIR)/etc/$${f##*/}" ; \
				install "$$f"/* "$(DESTDIR)/etc/$${f##*/}" ; \
				continue ; \
				fi ;\
			install -m 644 -t "$(DESTDIR)/etc" "$$f" ;\
			done; done
	set -e; for d in $(MODULES); do \
		[ -d "$$d/tools" ] || continue ; \
		mkdir -p "$(ULIB_PRE)$$d/" && \
		install "$$d/tools"/* "$(ULIB_PRE)$$d/" ; \
		done
	set -e ; for d in $(MODULES); do \
		if [ "$$d" = dyn-netconf ]; then module_number=05; else module_number=50; fi; \
		[ -d "$$d/dracut.modules.d" ] || continue; \
		mkdir -p "$(DESTDIR)$(DRACUT_D)/modules.d/$$module_number$$d"; \
		install -m 755 "$$d"/dracut.modules.d/*.sh "$(DESTDIR)$(DRACUT_D)/modules.d/$$module_number$$d/" ; \
		done
	mkdir -p "$(DESTDIR)/usr/sbin" "$(DESTDIR)/usr/share/man/man8"
	install -m 755 "overlayroot/usr/sbin/overlayroot-chroot" "$(DESTDIR)/usr/sbin"
	install -m 644 "overlayroot/usr/share/man/man8/overlayroot-chroot.8" "$(DESTDIR)/usr/share/man/man8"

#
# Fedora/EPEL
#

DRACUT_GROWROOT_D = dracut/modules.d/50growroot

install-fedora:
	mkdir -p "$(DESTDIR)/$(DRACUT_GROWROOT_D)"
	for f in growroot.sh module-setup.sh ; do \
		install "growroot/$(DRACUT_GROWROOT_D)/$$f" \
			"$(DESTDIR)/$(DRACUT_GROWROOT_D)/" ; \
	done

install-epel:
	mkdir -p "$(DESTDIR)/$(DRACUT_GROWROOT_D)"
	for f in growroot.sh install ; do \
		install "growroot/$(DRACUT_GROWROOT_D)/$$f" \
			"$(DESTDIR)/$(DRACUT_GROWROOT_D)/" ; \
	done

# vi: ts=4 noexpandtab syntax=make
