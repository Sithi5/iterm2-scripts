#!/usr/bin/env python3.7

import iterm2

white = (255, 255, 255)
cyberpunk_pink = (255, 0, 85)

class TabColorManager:
    def __init__(self):
        self.last_tab_session = None
        self.active_tab_color = iterm2.Color(*cyberpunk_pink) # Cyberpunk Pink
        self.default_tab_color = iterm2.Color(*white) # Light Grey
        self.change = iterm2.LocalWriteOnlyProfile()
        self.change.set_use_tab_color(True)

    async def update_tab_color(self, session):
        self.change.set_tab_color(self.default_tab_color)
        if self.last_tab_session is not None and self.last_tab_session != session:
            try:
                await self.last_tab_session.async_set_profile_properties(self.change)
            except iterm2.RPCException as e:
                print(f"Failed to set tab color for session\nError: {str(e)}")
        self.last_tab_session = session
        self.change.set_tab_color(self.active_tab_color)
        try:
            await session.async_set_profile_properties(self.change)
        except iterm2.RPCException as e:
            print(f"Failed to set tab color for session\nError: {str(e)}")

async def main(connection):
    app = await iterm2.async_get_app(connection)
    tab_color_manager = TabColorManager()
    await tab_color_manager.update_tab_color(app.current_terminal_window.current_tab.current_session)
    async with iterm2.FocusMonitor(connection) as monitor:
        while True:
            update = await monitor.async_get_next_update()
            if update.selected_tab_changed:
                await tab_color_manager.update_tab_color(app.current_terminal_window.current_tab.current_session)


# This instructs the script to run the "main" coroutine and to keep running even after it returns.
iterm2.run_forever(main)
