"""
Discovery Panel
Network device discovery interface
"""

import customtkinter as ctk
import logging
from typing import List, Callable
import threading

from models.device import Device, DeviceStatus
from utils.validators import validate_subnet, validate_ip_range


class DiscoveryPanel(ctk.CTkFrame):
    """Network discovery panel"""
    
    def __init__(self, parent, discovery_engine, connection_manager, credential_manager, status_callback: Callable = None):
        super().__init__(parent)
        
        self.logger = logging.getLogger(__name__)
        self.discovery_engine = discovery_engine
        self.connection_manager = connection_manager
        self.credential_manager = credential_manager
        self.status_callback = status_callback
        
        self.discovered_devices: List[Device] = []
        self.selected_devices: List[Device] = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup user interface"""
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="🔍 Network Discovery",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Input frame
        self._create_input_frame()
        
        # Results frame
        self._create_results_frame()
        
        # Actions frame
        self._create_actions_frame()
    
    def _create_input_frame(self):
        """Create input controls frame"""
        
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Subnet/Range label
        label = ctk.CTkLabel(
            input_frame,
            text="Network Range:",
            font=ctk.CTkFont(size=14)
        )
        label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Input field
        self.range_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="e.g., 192.168.1.0/24 or 192.168.1.1-192.168.1.50",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.range_input.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Scan button
        self.scan_button = ctk.CTkButton(
            input_frame,
            text="🔍 Scan Network",
            command=self._on_scan_click,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#3B8ED0", "#1F6AA5")
        )
        self.scan_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Add device manually button
        add_manual_button = ctk.CTkButton(
            input_frame,
            text="➕ Add Manually",
            command=self._add_device_manually,
            height=40,
            font=ctk.CTkFont(size=12),
            width=130
        )
        add_manual_button.grid(row=0, column=3, padx=10, pady=10)
        
        # Auto-detect LAN button
        auto_detect_button = ctk.CTkButton(
            input_frame,
            text="🌐 Auto-Detect LAN",
            command=self._auto_detect_lan,
            height=40,
            font=ctk.CTkFont(size=12),
            width=150,
            fg_color=("#2FA572", "#106A43")
        )
        auto_detect_button.grid(row=0, column=4, padx=10, pady=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(input_frame)
        self.progress_bar.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)
        
        # Status label
        self.scan_status_label = ctk.CTkLabel(
            input_frame,
            text="Enter a network range and click Scan",
            font=ctk.CTkFont(size=12)
        )
        self.scan_status_label.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10))
    
    def _create_results_frame(self):
        """Create results display frame"""
        
        results_frame = ctk.CTkFrame(self)
        results_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        # Results header
        header_frame = ctk.CTkFrame(results_frame)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)
        
        results_label = ctk.CTkLabel(
            header_frame,
            text="Discovered Devices (0)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Results table (using scrollable frame)
        self.results_scrollable = ctk.CTkScrollableFrame(results_frame)
        self.results_scrollable.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.results_scrollable.grid_columnconfigure(0, weight=1)
        
        # Table header
        self._create_table_header()
        
        self.results_label_ref = results_label
    
    def _create_table_header(self):
        """Create table header"""
        
        header_frame = ctk.CTkFrame(self.results_scrollable, fg_color=("#3B8ED0", "#1F6AA5"))
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        headers = [
            ("☑", 50),
            ("IP Address", 150),
            ("Hostname", 150),
            ("Vendor", 120),
            ("Status", 100),
            ("Credential", 120),
            ("Actions", 100)
        ]
        
        for idx, (header, width) in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width
            )
            label.grid(row=0, column=idx, padx=5, pady=5)
    
    def _create_actions_frame(self):
        """Create actions frame"""
        
        actions_frame = ctk.CTkFrame(self)
        actions_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Select all button
        select_all_btn = ctk.CTkButton(
            actions_frame,
            text="Select All",
            command=self._select_all_devices,
            width=120
        )
        select_all_btn.pack(side="left", padx=5, pady=10)
        
        # Deselect all button
        deselect_all_btn = ctk.CTkButton(
            actions_frame,
            text="Deselect All",
            command=self._deselect_all_devices,
            width=120
        )
        deselect_all_btn.pack(side="left", padx=5, pady=10)
        
        # Connect button
        self.connect_button = ctk.CTkButton(
            actions_frame,
            text="🔗 Connect Selected",
            command=self._on_connect_click,
            width=150,
            fg_color=("green", "darkgreen")
        )
        self.connect_button.pack(side="left", padx=5, pady=10)
        
        # Disconnect button
        self.disconnect_button = ctk.CTkButton(
            actions_frame,
            text="🔌 Disconnect All",
            command=self._on_disconnect_click,
            width=150,
            fg_color=("red", "darkred")
        )
        self.disconnect_button.pack(side="left", padx=5, pady=10)
        
        # Export button
        export_btn = ctk.CTkButton(
            actions_frame,
            text="💾 Export to CSV",
            command=self._export_to_csv,
            width=150
        )
        export_btn.pack(side="left", padx=5, pady=10)
        
        # Connection status
        self.connection_status_label = ctk.CTkLabel(
            actions_frame,
            text="Connected: 0",
            font=ctk.CTkFont(size=12)
        )
        self.connection_status_label.pack(side="right", padx=20, pady=10)
    
    def _on_scan_click(self):
        """Handle scan button click"""
        
        network_range = self.range_input.get().strip()
        
        if not network_range:
            self._show_error("Please enter a network range")
            return
        
        # Check if it's a single IP address and convert to CIDR
        try:
            import ipaddress
            ip_obj = ipaddress.ip_address(network_range)
            # Single IP - convert to /32 (single host)
            network_range = f"{network_range}/32"
            self._update_status(f"Scanning single IP: {ip_obj}")
            is_subnet = True
        except ValueError:
            # Not a single IP, validate as subnet or range
            is_subnet, subnet_error = validate_subnet(network_range)
            is_range, range_error = validate_ip_range(network_range)
            
            if not is_subnet and not is_range:
                self._show_error(f"Invalid input: {subnet_error or range_error}")
                return
        
        # Start scan in background thread
        self.scan_button.configure(state="disabled", text="⏳ Scanning...")
        self.progress_bar.set(0)
        
        thread = threading.Thread(target=self._perform_scan, args=(network_range, is_subnet))
        thread.daemon = True
        thread.start()
    
    def _perform_scan(self, network_range: str, is_subnet: bool):
        """Perform network scan in background"""
        
        try:
            self._update_status("Starting network scan...")
            
            def progress_callback(current, total):
                progress = current / total
                self.after(0, lambda: self.progress_bar.set(progress))
                self.after(0, lambda: self._update_status(f"Scanning... {current}/{total} hosts checked"))
            
            if is_subnet:
                devices = self.discovery_engine.discover_subnet(network_range, progress_callback)
            else:
                start_ip, end_ip = network_range.split('-')
                devices = self.discovery_engine.discover_ip_range(
                    start_ip.strip(),
                    end_ip.strip(),
                    progress_callback
                )
            
            self.discovered_devices = devices
            
            # Update UI on main thread
            self.after(0, self._update_results_table)
            
            # More helpful status message
            if len(devices) == 0:
                self.after(0, lambda: self._update_status(
                    "⚠️ Scan complete! Found 0 devices. "
                    "Check: 1) IP is correct 2) Device is powered on 3) Ping/ICMP is enabled 4) Network is reachable"
                ))
            else:
                self.after(0, lambda: self._update_status(f"✅ Scan complete! Found {len(devices)} device(s)"))
            
            self.after(0, lambda: self.progress_bar.set(1.0))
            
        except Exception as e:
            self.logger.error(f"Error during scan: {e}", exc_info=True)
            self.after(0, lambda: self._show_error(f"Scan failed: {str(e)}"))
        
        finally:
            self.after(0, lambda: self.scan_button.configure(state="normal", text="🔍 Scan Network"))
    
    def _update_results_table(self):
        """Update results table with discovered devices"""
        
        # Clear existing rows (except header)
        for widget in self.results_scrollable.winfo_children()[1:]:
            widget.destroy()
        
        # Update count
        self.results_label_ref.configure(text=f"Discovered Devices ({len(self.discovered_devices)})")
        
        # Add device rows
        for idx, device in enumerate(self.discovered_devices):
            self._add_device_row(idx + 1, device)
    
    def _add_device_row(self, row_idx: int, device: Device):
        """Add a device row to the table"""
        
        row_frame = ctk.CTkFrame(self.results_scrollable)
        row_frame.grid(row=row_idx, column=0, sticky="ew", pady=2)
        
        # Checkbox
        checkbox = ctk.CTkCheckBox(row_frame, text="", width=50, command=lambda: self._on_device_select(device))
        checkbox.grid(row=0, column=0, padx=5)
        device._checkbox = checkbox
        
        # IP Address
        ip_label = ctk.CTkLabel(row_frame, text=device.ip_address, width=150)
        ip_label.grid(row=0, column=1, padx=5)
        
        # Hostname
        hostname_label = ctk.CTkLabel(row_frame, text=device.hostname or "N/A", width=150)
        hostname_label.grid(row=0, column=2, padx=5)
        
        # Vendor
        vendor_label = ctk.CTkLabel(row_frame, text=device.vendor or "Unknown", width=120)
        vendor_label.grid(row=0, column=3, padx=5)
        
        # Status with color
        status_color = self._get_status_color(device.status)
        status_label = ctk.CTkLabel(
            row_frame,
            text=device.status.value,
            width=100,
            text_color=status_color
        )
        status_label.grid(row=0, column=4, padx=5)
        device._status_label = status_label
        
        # Credential dropdown
        credentials = self.credential_manager.list_credentials()
        cred_names = [c['name'] for c in credentials]
        
        if not cred_names:
            cred_names = ["No credentials"]
        
        cred_dropdown = ctk.CTkComboBox(
            row_frame,
            values=cred_names,
            width=120,
            command=lambda choice: self._on_credential_select(device, choice)
        )
        cred_dropdown.grid(row=0, column=5, padx=5)
        cred_dropdown.set(device.credential_name or cred_names[0])
        
        # Info button
        info_btn = ctk.CTkButton(
            row_frame,
            text="ℹ️",
            width=40,
            command=lambda: self._show_device_info(device)
        )
        info_btn.grid(row=0, column=6, padx=5)
    
    def _get_status_color(self, status: DeviceStatus) -> str:
        """Get color for device status"""
        colors = {
            DeviceStatus.REACHABLE: "green",
            DeviceStatus.CONNECTED: "lightgreen",
            DeviceStatus.UNREACHABLE: "red",
            DeviceStatus.DISCONNECTED: "orange",
            DeviceStatus.ERROR: "red",
            DeviceStatus.UNKNOWN: "gray"
        }
        return colors.get(status, "white")
    
    def _on_device_select(self, device: Device):
        """Handle device selection"""
        if hasattr(device, '_checkbox') and device._checkbox.get():
            if device not in self.selected_devices:
                self.selected_devices.append(device)
        else:
            if device in self.selected_devices:
                self.selected_devices.remove(device)
    
    def _on_credential_select(self, device: Device, credential_name: str):
        """Handle credential selection for device"""
        if credential_name != "No credentials":
            device.credential_name = credential_name
            self.logger.info(f"Assigned credential '{credential_name}' to {device.ip_address}")
    
    def _select_all_devices(self):
        """Select all devices"""
        self.selected_devices = self.discovered_devices.copy()
        for device in self.discovered_devices:
            if hasattr(device, '_checkbox'):
                device._checkbox.select()
    
    def _deselect_all_devices(self):
        """Deselect all devices"""
        self.selected_devices.clear()
        for device in self.discovered_devices:
            if hasattr(device, '_checkbox'):
                device._checkbox.deselect()
    
    def _on_connect_click(self):
        """Handle connect button click"""
        if not self.selected_devices:
            self._show_error("Please select at least one device")
            return
        
        # Connect in background
        thread = threading.Thread(target=self._connect_devices)
        thread.daemon = True
        thread.start()
    
    def _connect_devices(self):
        """Connect to selected devices"""
        success_count = 0
        
        for device in self.selected_devices:
            if not device.credential_name:
                self.logger.warning(f"No credential assigned to {device.ip_address}")
                continue
            
            self.after(0, lambda d=device: self._update_status(f"Connecting to {d.ip_address}..."))
            
            if self.connection_manager.connect(device):
                success_count += 1
                self.after(0, lambda d=device: self._update_device_status(d, DeviceStatus.CONNECTED))
        
        self.after(0, lambda: self._update_status(f"Connected to {success_count}/{len(self.selected_devices)} device(s)"))
        self.after(0, self._update_connection_count)
    
    def _on_disconnect_click(self):
        """Handle disconnect button click"""
        self.connection_manager.disconnect_all()
        
        for device in self.discovered_devices:
            if device.is_connected():
                self._update_device_status(device, DeviceStatus.DISCONNECTED)
        
        self._update_status("Disconnected from all devices")
        self._update_connection_count()
    
    def _update_device_status(self, device: Device, status: DeviceStatus):
        """Update device status in UI"""
        device.update_status(status)
        if hasattr(device, '_status_label'):
            device._status_label.configure(
                text=status.value,
                text_color=self._get_status_color(status)
            )
    
    def _update_connection_count(self):
        """Update connection status label"""
        count = self.connection_manager.get_active_connections_count()
        self.connection_status_label.configure(text=f"Connected: {count}")
    
    def _show_device_info(self, device: Device):
        """Show device information dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Device Info - {device.ip_address}")
        dialog.geometry("500x400")
        
        info_text = f"""
IP Address: {device.ip_address}
Hostname: {device.hostname or 'N/A'}
Vendor: {device.vendor or 'Unknown'}
Device Type: {device.device_type.value}
Model: {device.model or 'N/A'}
OS Version: {device.os_version or 'N/A'}
Status: {device.status.value}
Last Seen: {device.last_seen}
Credential: {device.credential_name or 'Not assigned'}
        """
        
        text_box = ctk.CTkTextbox(dialog, width=480, height=350)
        text_box.pack(padx=10, pady=10)
        text_box.insert("1.0", info_text)
        text_box.configure(state="disabled")
    
    def _export_to_csv(self):
        """Export discovered devices to CSV"""
        if not self.discovered_devices:
            self._show_error("No devices to export")
            return
        
        from datetime import datetime
        import csv
        from pathlib import Path
        
        filename = f"discovered_devices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = Path("reports") / filename
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['IP Address', 'Hostname', 'Vendor', 'Device Type', 'Status', 'Last Seen'])
                
                for device in self.discovered_devices:
                    writer.writerow([
                        device.ip_address,
                        device.hostname or 'N/A',
                        device.vendor or 'Unknown',
                        device.device_type.value,
                        device.status.value,
                        device.last_seen
                    ])
            
            self._update_status(f"Exported to {filepath}")
        except Exception as e:
            self._show_error(f"Export failed: {str(e)}")
    
    def _update_status(self, message: str):
        """Update status label"""
        self.scan_status_label.configure(text=message)
        if self.status_callback:
            self.status_callback(message)
    
    def _show_error(self, message: str):
        """Show error message"""
        self.scan_status_label.configure(text=f"❌ {message}", text_color="red")
        self.logger.error(message)
    
    def _add_device_manually(self):
        """Add device manually without ping"""
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Device Manually")
        dialog.geometry("450x300")
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # IP Address
        ctk.CTkLabel(form_frame, text="IP Address:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ip_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g., 10.192.173.181")
        ip_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Hostname (optional)
        ctk.CTkLabel(form_frame, text="Hostname:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        hostname_entry = ctk.CTkEntry(form_frame, placeholder_text="Optional")
        hostname_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Vendor
        ctk.CTkLabel(form_frame, text="Vendor:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        vendor_dropdown = ctk.CTkComboBox(
            form_frame,
            values=["Cisco", "Juniper", "HP", "Huawei", "Arista", "MikroTik", "Ubiquiti", "Other"]
        )
        vendor_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        vendor_dropdown.set("Cisco")
        
        # Info label
        info_label = ctk.CTkLabel(
            form_frame,
            text="💡 Use this to add devices that don't respond to ping\nbut are reachable via SSH",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10)
        
        def add_device():
            ip = ip_entry.get().strip()
            
            if not ip:
                error_label = ctk.CTkLabel(
                    form_frame,
                    text="❌ IP address is required",
                    text_color="red"
                )
                error_label.grid(row=4, column=0, columnspan=2)
                return
            
            # Validate IP
            try:
                import ipaddress
                ipaddress.ip_address(ip)
            except ValueError:
                error_label = ctk.CTkLabel(
                    form_frame,
                    text="❌ Invalid IP address format",
                    text_color="red"
                )
                error_label.grid(row=4, column=0, columnspan=2)
                return
            
            # Create device
            from models.device import Device, DeviceStatus, DeviceType
            
            # Get vendor and set appropriate device type
            vendor_name = vendor_dropdown.get()
            device_type = DeviceType.UNKNOWN
            
            if vendor_name == "Cisco":
                device_type = DeviceType.ROUTER  # Default to router
            elif vendor_name in ["Juniper", "HP", "Huawei", "Arista"]:
                device_type = DeviceType.SWITCH
            
            device = Device(
                ip_address=ip,
                hostname=hostname_entry.get().strip() or None,
                vendor=vendor_name if vendor_name != "Other" else None,
                device_type=device_type,
                status=DeviceStatus.REACHABLE
            )
            
            # Add to discovered devices
            self.discovered_devices.append(device)
            
            # Log the addition
            self.logger.info(f"Manually added device: {ip}")
            
            # Update UI on main thread
            self.after(0, self._update_results_table)
            self.after(0, lambda: self._update_status(f"✅ Manually added device: {ip}"))
            
            # Close dialog
            dialog.destroy()
        
        ctk.CTkButton(
            button_frame,
            text="➕ Add Device",
            command=add_device,
            fg_color=("green", "darkgreen")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=5)
    
    def _auto_detect_lan(self):
        """Auto-detect connected LAN and scan all devices"""
        import socket
        import subprocess
        import re
        
        try:
            # Get network interfaces using ipconfig on Windows
            result = subprocess.run(['ipconfig'], capture_output=True, text=True, shell=True)
            output = result.stdout
            
            # Parse ipconfig output to find active network adapters
            detected_networks = []
            current_adapter = None
            current_ip = None
            current_mask = None
            
            for line in output.split('\n'):
                line = line.strip()
                
                # Detect adapter name
                if 'adapter' in line.lower() and ':' in line:
                    current_adapter = line.split(':')[0].strip()
                    current_ip = None
                    current_mask = None
                
                # Detect IPv4 address
                if 'IPv4 Address' in line or 'IPv4 address' in line:
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if match:
                        current_ip = match.group(1)
                
                # Detect subnet mask
                if 'Subnet Mask' in line:
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if match:
                        current_mask = match.group(1)
                
                # If we have both IP and mask, add to list
                if current_ip and current_mask and current_adapter:
                    # Skip loopback
                    if not current_ip.startswith('127.'):
                        detected_networks.append({
                            'interface': current_adapter,
                            'ip': current_ip,
                            'netmask': current_mask
                        })
                        current_ip = None
                        current_mask = None
            
            if not detected_networks:
                self._update_status("❌ No active network interfaces found")
                return
            
            # Create selection dialog
            dialog = ctk.CTkToplevel(self)
            dialog.title("Auto-Detect LAN")
            dialog.geometry("600x400")
            dialog.transient(self)
            dialog.grab_set()
            
            # Center dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
            y = (dialog.winfo_screenheight() // 2) - (400 // 2)
            dialog.geometry(f"+{x}+{y}")
            
            # Title
            title_label = ctk.CTkLabel(
                dialog,
                text="🌐 Auto-Detect LAN Networks",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title_label.pack(pady=20)
            
            # Info label
            info_label = ctk.CTkLabel(
                dialog,
                text="Select a network to scan all devices on that LAN:",
                font=ctk.CTkFont(size=12)
            )
            info_label.pack(pady=10)
            
            # Network list frame
            list_frame = ctk.CTkScrollableFrame(dialog, width=550, height=200)
            list_frame.pack(pady=10, padx=20, fill="both", expand=True)
            
            selected_network = {"value": None}
            buttons = []
            
            def calculate_cidr(ip, netmask):
                """Calculate CIDR notation from IP and netmask"""
                import ipaddress
                try:
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                    return str(network)
                except:
                    return f"{ip}/24"
            
            def on_network_select(net_info, button):
                selected_network["value"] = net_info
                # Reset all buttons
                for btn in buttons:
                    btn.configure(fg_color=("#3B8ED0", "#1F6AA5"))
                # Highlight selected
                button.configure(fg_color=("green", "darkgreen"))
                
            # Display detected networks
            for i, net_info in enumerate(detected_networks):
                cidr = calculate_cidr(net_info['ip'], net_info['netmask'])
                
                net_button = ctk.CTkButton(
                    list_frame,
                    text=f"🌐 {net_info['interface']}\n📡 Network: {cidr}\n💻 Your IP: {net_info['ip']}",
                    height=70,
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                net_button.configure(command=lambda n=net_info, b=net_button: on_network_select(n, b))
                net_button.pack(pady=5, padx=10, fill="x")
                buttons.append(net_button)
            
            # Button frame
            button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
            button_frame.pack(pady=20)
            
            def start_scan():
                if not selected_network["value"]:
                    info_label.configure(text="⚠️ Please select a network first!", text_color="red")
                    return
                
                net_info = selected_network["value"]
                cidr = calculate_cidr(net_info['ip'], net_info['netmask'])
                
                # Close dialog
                dialog.destroy()
                
                # Set the network range in the input field
                self.network_entry.delete(0, "end")
                self.network_entry.insert(0, cidr)
                
                # Update status
                self._update_status(f"🌐 Auto-detected LAN: {cidr} on {net_info['interface']}")
                
                # Start the scan automatically
                self._on_scan_click()
            
            ctk.CTkButton(
                button_frame,
                text="🔍 Scan Selected Network",
                command=start_scan,
                fg_color=("green", "darkgreen"),
                width=200,
                height=40
            ).pack(side="left", padx=5)
            
            ctk.CTkButton(
                button_frame,
                text="Cancel",
                command=dialog.destroy,
                width=100,
                height=40
            ).pack(side="left", padx=5)
            
        except Exception as e:
            self.logger.error(f"Error auto-detecting LAN: {str(e)}")
            self._update_status(f"❌ Error auto-detecting LAN: {str(e)}")
    
    def get_discovered_devices(self) -> List[Device]:
        """Get list of discovered devices"""
        return self.discovered_devices
    
    def refresh(self):
        """Refresh the panel"""
        self._update_results_table()
        self._update_connection_count()
