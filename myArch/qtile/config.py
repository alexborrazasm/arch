from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os, subprocess

#themes colors:
color_white= "#ffffff"
color_black= "#2e2929"
color_background= "#1a1b26"
color_unfocus= "#16161a"
color_arch= "#1793d1"
color_cpu= color_arch
color_ram= "#420f3d"
color_net= "#22ab57"
use_font= "Hack Nerd Font"
use_opacity= 0.95
size_bar= 26

mod = "mod4"
terminal = guess_terminal("kitty")

#functions
def get_border(select,icon_color,back_color): #rounds the edges
    if select==1:
        icon=""
        size=size_bar*1.4
    else:
        icon=""
        size=size_bar*1.2
    return widget.TextBox(
        text=icon,
        fontsize=size,
        foreground=icon_color,
        background=back_color,
        padding=-3,
    )

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), lazy.layout.reset(), desc="Reset all window sizes"),
    Key([ "Mod4" ], "plus", lazy.layout.grow(), desc="Grow window"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Launch menu apps"),
    #Brightness
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10"), desc="Brightness down"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 10"), desc="Brightness up"),
    # Volume1
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q sset Master 5%-"), desc="Volume down"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q sset Master 5%+"), desc="Volume up"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q sset Master toggle"), desc="Volume mute"),
    Key([mod], "l", lazy.spawn("light-locker-command -l"), desc="Lock Screen"),
    Key([mod], "i", lazy.spawn("xcolor -s"), desc="xcolor tool"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Rofi greenclip
    Key(["control", "mod1"], "Tab", lazy.spawn("rofi -modi 'clipboard:greenclip print' -show clipboard -run-command '{cmd}'")),
]

groups = [Group(i) for i in [
    "Net", "Dev", "Term", "Med", "Soc", "1", "2", "3", "4"
]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

layout_theme = {
    "border_focus": color_arch,
    "border_width":1,
    "single_border_width": 0,
    "margin": 0,
    "single_margin": 0,
    "border_normal": color_unfocus,
    "grow_amount": 4,
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
]

widget_defaults = dict(
    font=use_font,
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

screens = [
    #built-in screen
    Screen(
        top=bar.Bar(
            [   
                widget.TextBox(
                    "󰣇",
                    foreground=color_arch,
                    fontsize=20,
                    padding=6,
                ),
                widget.GroupBox(
                    highlight_method="line",
                    highlight_color=[color_background, color_background],
                    this_current_screen_border=color_arch,
                    visible_groups=["Net","Dev","Term","Med","Soc"],
                ),
                widget.WindowName(),
                widget.Systray(padding=6),
                widget.Volume(volume_app='pavucontrol',padding=0),
                get_border(2,color_cpu, color_background),
                widget.CPU(
                    background=color_cpu,
                    foreground=color_white,
                    format=' {freq_current}GHz {load_percent}%',
                ),
                widget.ThermalSensor(background=color_cpu, foreground=color_white),
                get_border(1,color_ram, color_cpu),
                widget.Memory(
                    background=color_ram,
                    foreground=color_white,
                    format='{MemUsed:.1f}GB/{MemTotal:.1f}GB',
                    measure_mem='G',
                ),
                get_border(1,color_net, color_ram),
                widget.Net(
                    background=color_net,
                    foreground=color_white,
                    format='{up} ↑↓{down}',
                    prefix='M',
                ),
                get_border(1,color_background, color_net),
                widget.Clock(format="%d-%m-%Y %H:%M "),
                widget.TextBox(" ", width=1),
                ],
                size_bar,
                opacity=use_opacity,
                background=color_background,
                margin=0,
            ),
        ),
    #add-on screen
    Screen(
        top=bar.Bar(
            [   
                widget.TextBox(
                    "󰣇",
                    foreground=color_arch,
                    fontsize=20,
                    padding=6,
                ),
                widget.GroupBox(
                    highlight_method="line",
                    highlight_color=[color_background, color_background],
                    this_current_screen_border=color_arch,
                    visible_groups=["Net","Dev","Term","Med","Soc"],
                ),
                widget.WindowName(),
                get_border(2,color_cpu, color_background),
                widget.CPU(
                    background=color_cpu,
                    foreground=color_white,
                    format=' {freq_current}GHz {load_percent}%',
                ),
                widget.ThermalSensor(background=color_cpu, foreground=color_white),
                get_border(1,color_ram, color_cpu),
                widget.Memory(
                    background=color_ram,
                    foreground=color_white,
                    format='{MemUsed:.1f}GB/{MemTotal:.1f}GB',
                    measure_mem='G',
                ),
                get_border(1,color_net, color_ram),
                widget.Net(
                    background=color_net,
                    foreground=color_white,
                    format='{up} ↑↓{down}',
                    prefix='M',
                ),
                get_border(1,color_background, color_net),
                widget.Clock(format="%d-%m-%Y %H:%M "),
                widget.TextBox(" ", width=1),
                ],
                size_bar,
                opacity=use_opacity,
                background=color_background,
                margin=0,
            ),
        ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    #Click([mod], "Button2", lazy.window.bring_to_front()),
    Click([mod], "Button2", lazy.window.toggle_floating()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(**layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])