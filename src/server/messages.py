"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

import logging

from .epa_constants import EPACommand


logger = logging.getLogger(__name__)


class DeviceStatus:
    """Device Status.

    Attributes
    ----------
    EPA_COMMAND_DEVICE_STATUS_MESSAGES  Status Message.

    Methods
    -------
    get_device_status_message()         Status Message, sent back to the Client.

    """

    EPA_COMMAND_DEVICE_STATUS_MESSAGES = (
        (EPACommand.DEVICE_CLAIMED, "Device claim "),
        (EPACommand.DEVICE_SAVE_FILE, "Device file save"))

    @classmethod
    def get_device_status_message(cls, command):
        """Status Message, sent back to the Client.

        Parameters
        ----------
        command         : str           Command.

        """
        for choice in cls.EPA_COMMAND_DEVICE_STATUS_MESSAGES:
            if command == choice[0]:
                return choice[1]

        return ""
