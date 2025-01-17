import sys
sys.path.append('/app')
from timer import *
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class TimerWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, title=timer_title)
        self.set_border_width(40)
        print(timer_running)

        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(mainBox)

        self.spinner = Gtk.Spinner()
        mainBox.pack_start(self.spinner, True, True, 0)

        self.label = Gtk.Label()
        mainBox.pack_start(self.label, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text("10")
        mainBox.pack_start(self.entry, True, True, 0)

        self.buttonStart = Gtk.Button(label=run_timer)
        self.buttonStart.connect("clicked", self.on_buttonStart_clicked)
        mainBox.pack_start(self.buttonStart, True, True, 0)

        self.buttonStop = Gtk.Button(label=stop_timer)
        self.buttonStop.set_sensitive(False)
        self.buttonStop.connect("clicked", self.on_buttonStop_clicked)
        mainBox.pack_start(self.buttonStop, True, True, 0)

        self.timeout_id = None
        self.connect("destroy", self.on_SpinnerWindow_destroy)

    def on_buttonStart_clicked(self, widget, *args):
        """ button "clicked" in event buttonStart. """
        self.start_timer()

    def on_buttonStop_clicked(self, widget, *args):
        """ button "clicked" in event buttonStop. """
        self.stop_timer("Timer has been stopped")

    def on_SpinnerWindow_destroy(self, widget, *args):
        """ procesing closing window """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        Gtk.main_quit()

    def on_timeout(self, *args, **kwargs):
        """ Features timer limit.
        """

        self.counter -= 1
        if self.counter <= 0:
            self.stop_timer(timing_finished)
            print(timing_finished)
            return False
        self.label.set_label(time_text + str(int(self.counter / 4)) + " s")
        return True


    def start_timer(self):
        """ Run Timer. """
        self.buttonStart.set_sensitive(False)
        self.buttonStop.set_sensitive(True)
        self.counter = 4 * int(self.entry.get_text())
        self.label.set_label(time_text + str(int(self.counter / 4)))
        self.spinner.start()
        self.timeout_id = GLib.timeout_add(250, self.on_timeout, None)
        print(timing_ended)

    def stop_timer(self, alabeltext):
        """ Stop Timer """
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.spinner.stop()
        self.buttonStart.set_sensitive(True)
        self.buttonStop.set_sensitive(False)
        self.label.set_label(alabeltext)
        print(timing_ended)


win = TimerWindow()
win.show_all()
Gtk.main()
print(timer_quit)
