"""
Unit tests for time_parser utilities.
"""
import unittest
from datetime import datetime, timedelta
import pytz
from utils.time_parser import (
    parse_natural_time,
    parse_relative_time,
    generate_discord_timestamp,
    get_all_format_examples
)


class TestTimeParser(unittest.TestCase):
    """Test cases for time parsing functions."""
    
    def test_parse_natural_time_today(self):
        """Test parsing 'today 3pm' with different timezones."""
        # Test with New York timezone
        result = parse_natural_time("today 3pm", "America/New_York")
        self.assertEqual(result.hour, 15)
        self.assertEqual(result.tzinfo.zone, "America/New_York")
        
    def test_parse_natural_time_tomorrow(self):
        """Test parsing 'tomorrow'."""
        result = parse_natural_time("tomorrow", "UTC")
        now = datetime.now(pytz.UTC)
        # Should be approximately 1 day from now
        diff = (result - now).days
        self.assertIn(diff, [0, 1])  # Could be today or tomorrow depending on time
        
    def test_parse_natural_time_with_timezone(self):
        """Test that timezone is correctly applied."""
        result = parse_natural_time("today noon", "Asia/Tokyo")
        self.assertEqual(result.hour, 12)
        self.assertEqual(result.tzinfo.zone, "Asia/Tokyo")
        
    def test_parse_natural_time_invalid(self):
        """Test that invalid time strings raise ValueError."""
        with self.assertRaises(ValueError):
            parse_natural_time("xyz invalid time", "UTC")
    
    def test_parse_natural_time_invalid_timezone(self):
        """Test that invalid timezones raise ValueError."""
        with self.assertRaises(ValueError):
            parse_natural_time("today 3pm", "Invalid/Timezone")
    
    def test_parse_relative_time_hours(self):
        """Test parsing hours."""
        now = datetime.now(pytz.UTC)
        result = parse_relative_time("2 hours")
        
        # Should be approximately 2 hours from now
        diff = (result - now).total_seconds()
        self.assertAlmostEqual(diff, 2 * 3600, delta=5)
    
    def test_parse_relative_time_minutes(self):
        """Test parsing minutes."""
        now = datetime.now(pytz.UTC)
        result = parse_relative_time("30 minutes")
        
        # Should be approximately 30 minutes from now
        diff = (result - now).total_seconds()
        self.assertAlmostEqual(diff, 30 * 60, delta=5)
    
    def test_parse_relative_time_combined(self):
        """Test parsing combined hours and minutes."""
        now = datetime.now(pytz.UTC)
        result = parse_relative_time("2 hours 15 minutes")
        
        # Should be approximately 2h 15m from now
        diff = (result - now).total_seconds()
        expected = (2 * 3600) + (15 * 60)
        self.assertAlmostEqual(diff, expected, delta=5)
    
    def test_parse_relative_time_abbreviations(self):
        """Test parsing with abbreviations."""
        now = datetime.now(pytz.UTC)
        result = parse_relative_time("1h 30m")
        
        # Should be approximately 1h 30m from now
        diff = (result - now).total_seconds()
        expected = 3600 + (30 * 60)
        self.assertAlmostEqual(diff, expected, delta=5)
    
    def test_parse_relative_time_invalid(self):
        """Test that invalid duration strings raise ValueError."""
        with self.assertRaises(ValueError):
            parse_relative_time("invalid duration")
    
    def test_generate_discord_timestamp(self):
        """Test Discord timestamp generation."""
        # Create a known datetime
        dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
        timestamp = int(dt.timestamp())
        
        # Test default format
        result = generate_discord_timestamp(dt)
        self.assertEqual(result, f"<t:{timestamp}:F>")
        
        # Test specific format
        result = generate_discord_timestamp(dt, "R")
        self.assertEqual(result, f"<t:{timestamp}:R>")
    
    def test_get_all_format_examples(self):
        """Test getting all format examples."""
        dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
        formats = get_all_format_examples(dt)
        
        # Should have all 7 formats
        self.assertEqual(len(formats), 7)
        
        # Check that keys are present
        expected_keys = [
            "Short Time", "Long Time", "Short Date", "Long Date",
            "Short Date/Time", "Long Date/Time", "Relative"
        ]
        for key in expected_keys:
            self.assertIn(key, formats)
        
        # Check format structure
        for name, (code, timestamp_str) in formats.items():
            self.assertIsInstance(code, str)
            self.assertIsInstance(timestamp_str, str)
            self.assertTrue(timestamp_str.startswith("<t:"))
            self.assertTrue(timestamp_str.endswith(f":{code}>"))


if __name__ == "__main__":
    unittest.main()
