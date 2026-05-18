# Legacy CSCS SSH Service CLI — Discontinued

> [!CAUTION]
> **This service has been fully discontinued.**
> This repository is no longer maintained, and the underlying CSCS SSH Service CLI is no longer in operation. This repository is kept online for historical reference only and will be archived.

## Current SSH workflow at CSCS

SSH key management is now handled entirely through the new User Account portal and the new CLI:

- **User Account portal**: https://user-account.cscs.ch
- **New CLI repository**: https://github.com/eth-cscs/cscs-key
- **Documentation**: https://docs.cscs.ch/access/ssh/

From the User Account portal, users can manage account information, personal data, and SSH keys, as well as **sign their own SSH key** — a capability not available in this legacy CLI.

## What happened

As part of the modernization of the CSCS IAM layer, the legacy SSH Service was replaced by a new system integrated with the User Account portal. The CLI was fully rewritten and redesigned to provide a better user experience.

Following the migration, the legacy service has now been fully decommissioned. The code in this repository no longer corresponds to any running service and will not function against current CSCS infrastructure.

## Repository status

> [!IMPORTANT]
> This repository is **deprecated, unmaintained, and scheduled for archival**. No issues, pull requests, or support requests will be processed.

Please update any bookmarks, scripts, internal references, or documentation that still point to this repository.

## Support

For all current SSH-related workflows, please refer to the new CLI repository, the User Account portal, and the updated documentation linked above.
