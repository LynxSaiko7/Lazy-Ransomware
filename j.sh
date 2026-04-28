cat > /etc/pam.d/login << 'EOF'
#%PAM-1.0
auth       requisite  pam_securetty.so
auth       include    system-auth
account    include    system-account
password   include    system-password
session    include    system-session
EOF
