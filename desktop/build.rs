fn main() {
    // Every command is named, so each window only gets the ones its capability file lists (capabilities/).
    let commands = &[
        "robot_state", "robot_grab", "robot_drag", "robot_drop", "robot_click", "robot_menu", "robot_take", "robot_list", "robot_given", "box_given",
        "box_state", "box_look", "box_fit", "box_draft", "box_close", "connect", "sign_in", "add_todo", "add_file", "remove_file",
        "take_screenshot", "todo_quick", "todo_decide", "todo_undo", "ask", "open_dashboard", "menu_item", "card_open", "card_place", "card_close",
        "set_speaks", "bubble_state", "bubble_fit", "bubble_hold", "bubble_open", "bubble_join", "bubble_done",
        "robot_notify", "app_state", "app_retry", "settings_state", "settings_set", "settings_fit", "update_apply",
    ];
    if std::env::var("CARGO_CFG_TARGET_OS").as_deref() == Ok("linux") {
        // libgtk-layer-shell.so.0 from the system, or from lib/ next to the program
        println!("cargo:rustc-link-arg-bins=-Wl,-rpath,$ORIGIN/lib");
    }
    tauri_build::try_build(
        tauri_build::Attributes::new().app_manifest(tauri_build::AppManifest::new().commands(commands)),
    )
    .expect("tauri build");
}
