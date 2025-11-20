package org.dimensionalcortex.app;

import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.content.Intent;
import android.content.Context;
import android.util.Log;
import android.os.Bundle;
import java.util.List;
import java.util.ArrayList;

public class UDACAccessibilityService extends AccessibilityService {
    private static final String TAG = "UDACService";
    public static final String ACTION_ACCESSIBILITY_EVENT = "org.dimensionalcortex.app.ACCESSIBILITY_EVENT";
    public static final String EXTRA_EVENT_TYPE = "event_type";
    public static final String EXTRA_PACKAGE_NAME = "package_name";
    public static final String EXTRA_CLASS_NAME = "class_name";
    public static final String EXTRA_TEXT = "text";
    public static final String EXTRA_IS_EDITABLE = "is_editable";
    public static final String EXTRA_CONTENT_DESCRIPTION = "content_description";

    @Override
    public void onServiceConnected() {
        Log.i(TAG, "Service connected");
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        try {
            if (event == null) return;

            // Create intent to broadcast to Python
            Intent intent = new Intent(ACTION_ACCESSIBILITY_EVENT);
            intent.putExtra(EXTRA_EVENT_TYPE, event.getEventType());

            if (event.getPackageName() != null) {
                intent.putExtra(EXTRA_PACKAGE_NAME, event.getPackageName().toString());
            }

            if (event.getClassName() != null) {
                intent.putExtra(EXTRA_CLASS_NAME, event.getClassName().toString());
            }

            // Check if source is editable
            boolean isEditable = false;
            AccessibilityNodeInfo source = event.getSource();
            if (source != null) {
                isEditable = source.isEditable();
                // Don't recycle immediately if we were to use it more,
                // but here we just check one property.
                // source.recycle(); // Good practice to recycle, but handled by GC usually in simple cases.
            }
            intent.putExtra(EXTRA_IS_EDITABLE, isEditable);

            // Extract text content
            List<CharSequence> textList = event.getText();
            if (textList != null && !textList.isEmpty()) {
                StringBuilder sb = new StringBuilder();
                for (CharSequence text : textList) {
                    if (text != null) {
                        sb.append(text);
                        sb.append("\n");
                    }
                }
                intent.putExtra(EXTRA_TEXT, sb.toString().trim());
            }

            if (event.getContentDescription() != null) {
                intent.putExtra(EXTRA_CONTENT_DESCRIPTION, event.getContentDescription().toString());
            }

            // Send broadcast so Python (Kivy) can pick it up
            sendBroadcast(intent);

        } catch (Exception e) {
            Log.e(TAG, "Error processing accessibility event", e);
        }
    }

    @Override
    public void onInterrupt() {
        Log.i(TAG, "Service interrupted");
    }
}
